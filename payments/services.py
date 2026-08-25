import logging
from datetime import timedelta
from decimal import Decimal

import stripe
from django.conf import settings
from django.db import transaction
from django.utils import timezone

from content.enums import BookingStatus, PaymentMethod
from content.models import Consultation
from engagement.models import Booking

from .models import Payment, PaymentStatus

logger = logging.getLogger(__name__)


class PaymentServiceError(Exception):
    """Raised when a payment cannot be created/processed."""


def _stripe():
    if not settings.STRIPE_SECRET_KEY:
        raise PaymentServiceError('Stripe is not configured (missing STRIPE_SECRET_KEY).')
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return stripe


def compute_payment_amount(consultation: Consultation) -> Decimal:
    """Server-side total (fee + processing_fee - discount). Never trusts the client."""
    if consultation.is_free:
        return Decimal('0')
    amount = (consultation.fee or 0) + (consultation.processing_fee or 0) - (consultation.discount or 0)
    return max(Decimal(amount).quantize(Decimal('0.01')), Decimal('0'))


def _to_charge_payment_method(charge) -> str:
    """Best-effort map from a Stripe charge to our PaymentMethod enum.

    Apple Pay surfaces as a card wallet, so both still map from charge details
    after the fact rather than being declared by the client.
    """
    try:
        details = charge.get('payment_method_details') or {}
        ptype = details.get('type')
        if ptype == 'card':
            card = details.get('card') or {}
            wallet = card.get('wallet') or {}
            if wallet.get('type') == 'apple_pay':
                return PaymentMethod.APPLE_PAY
            return PaymentMethod.CARD
        # Any other method (e.g. an external wallet) is stored verbatim-safe as card.
        return PaymentMethod.CARD
    except Exception:  # pragma: no cover - defensive
        return PaymentMethod.CARD


def create_payment_intent(consultation: Consultation, booking_data: dict) -> dict:
    """Create a Stripe PaymentIntent + a pending booking that reserves the seat.

    ``booking_data`` carries the contact fields (fullName/contactNumber/email/...).
    The amount is always recomputed server-side.
    """
    if consultation.status != 'Published' or not consultation.is_bookable:
        raise PaymentServiceError('This consultation session is not available for booking.')

    seats = booking_data.get('seats') or 1
    seats_left = consultation.seats_left
    if seats_left is not None and seats > max(seats_left, 0):
        raise PaymentServiceError('Not enough seats available for this session.')

    amount = compute_payment_amount(consultation)
    if amount <= 0:
        raise PaymentServiceError('This session does not require payment.')

    client = _stripe()
    booking = Booking(**booking_data)
    booking.consultation = consultation
    booking.status = BookingStatus.PENDING_PAYMENT
    booking.amount = amount
    booking.payment_success = False
    booking.expires_at = timezone.now() + timedelta(seconds=settings.BOOKING_PENDING_TTL_SECONDS)
    booking.save()

    amount_cents = int(amount * 100)
    try:
        intent = client.PaymentIntent.create(
            amount=amount_cents,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                'booking_reference': booking.reference,
                'consultation_id': str(consultation.pk),
            },
            automatic_payment_methods={'enabled': True},
        )
    except Exception as exc:
        logger.exception('Stripe PaymentIntent.create failed for %s', booking.reference)
        booking.delete()
        raise PaymentServiceError('Could not initialize payment. Please try again.') from exc

    payment = Payment.objects.create(
        booking=booking,
        stripe_payment_intent_id=intent['id'],
        client_secret=intent['client_secret'],
        amount=amount,
        currency=settings.STRIPE_CURRENCY,
    )
    logger.info('PaymentIntent %s created for booking %s (%s)', intent['id'], booking.reference, amount)

    return {
        'paymentIntentId': intent['id'],
        'clientSecret': intent['client_secret'],
        'amount': int(amount_cents),
        'currency': settings.STRIPE_CURRENCY,
        'bookingReference': booking.reference,
    }


@transaction.atomic
def confirm_booking_payment(stripe_payment_intent_id: str) -> Booking:
    """Confirm a booking once a PaymentIntent has succeeded.

    Idempotent: if the booking is already CONFIRMED it is returned untouched so a
    raced webhook + client-confirm pair cannot double-fire. Rows are locked with
    ``select_for_update`` to serialize concurrent transitions.
    """
    payment = Payment.objects.select_for_update().filter(
        stripe_payment_intent_id=stripe_payment_intent_id
    ).first()
    if not payment:
        raise PaymentServiceError('Payment intent not found for this booking.')

    booking = Booking.objects.select_for_update().select_related('consultation').get(pk=payment.booking_id)
    if booking.status == BookingStatus.CONFIRMED and booking.payment_success:
        return booking

    client = _stripe()
    intent = client.PaymentIntent.retrieve(stripe_payment_intent_id)
    if intent['status'] != 'succeeded':
        raise PaymentServiceError('Payment has not succeeded yet.')

    booking.status = BookingStatus.CONFIRMED
    booking.payment_success = True
    booking.payment_reference = stripe_payment_intent_id
    booking.expires_at = None
    charges = intent.get('charges', {}).get('data', [])
    if charges:
        booking.payment_method = _to_charge_payment_method(charges[-1])
    booking.save()

    payment.status = PaymentStatus.SUCCEEDED
    payment.amount = Decimal(str(intent['amount'] / 100)).quantize(Decimal('0.01'))
    payment.save()

    payment.booking = booking
    payment.save(update_fields=['booking', 'status', 'amount'])

    logger.info('Booking %s confirmed via PaymentIntent %s', booking.reference, stripe_payment_intent_id)
    return booking


def mark_payment_failed(stripe_payment_intent_id: str) -> None:
    """Mark a payment failed and cancel its pending booking, releasing the seat."""
    with transaction.atomic():
        payment = Payment.objects.select_for_update().filter(
            stripe_payment_intent_id=stripe_payment_intent_id
        ).first()
        if not payment:
            return
        payment.status = PaymentStatus.FAILED
        payment.save()

        booking = Booking.objects.select_for_update().get(pk=payment.booking_id)
        if booking.status == BookingStatus.PENDING_PAYMENT:
            booking.status = BookingStatus.CANCELLED
            booking.expires_at = None
            booking.save()


def cancel_booking(booking: Booking) -> None:
    """Cancel a pending booking and cancel its Stripe PaymentIntent (seat release)."""
    with transaction.atomic():
        locked = Booking.objects.select_for_update().get(pk=booking.pk)
        if locked.status != BookingStatus.PENDING_PAYMENT:
            return

        payment = Payment.objects.select_for_update().filter(booking=locked).first()
        if payment and payment.status == PaymentStatus.PENDING:
            try:
                _stripe().PaymentIntent.cancel(payment.stripe_payment_intent_id)
            except Exception as exc:  # pragma: no cover - Stripe may already have closed it
                logger.warning('Could not cancel PaymentIntent %s: %s', payment.stripe_payment_intent_id, exc)
            payment.status = PaymentStatus.CANCELED
            payment.save(update_fields=['status'])

        locked.status = BookingStatus.CANCELLED
        locked.expires_at = None
        locked.save(update_fields=['status', 'expires_at'])


def release_expired_bookings() -> int:
    """Cancel any pending bookings past their expiry, releasing held seats."""
    expired = Booking.objects.filter(
        status=BookingStatus.PENDING_PAYMENT,
        expires_at__lte=timezone.now(),
    )
    count = 0
    for booking in expired:
        cancel_booking(booking)
        count += 1
    if count:
        logger.info('Released %s expired pending booking(s).', count)
    return count


def handle_stripe_webhook_event(event) -> None:
    """Route a verified Stripe event by type. Shared authoritative confirmation path."""
    event_type = event['type']
    payment_intent_id = event['data']['object'].get('id')

    if event_type == 'payment_intent.succeeded':
        if payment_intent_id:
            try:
                confirm_booking_payment(payment_intent_id)
            except PaymentServiceError as exc:
                logger.warning('Webhook confirm skipped for %s: %s', payment_intent_id, exc)
    elif event_type == 'payment_intent.payment_failed':
        if payment_intent_id:
            mark_payment_failed(payment_intent_id)
    else:
        logger.info('Ignoring unhandled Stripe event %s', event_type)

