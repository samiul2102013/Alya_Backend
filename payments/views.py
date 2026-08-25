import logging

import stripe
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from engagement.serializers import BookingSerializer

from . import services

logger = logging.getLogger(__name__)


class CreatePaymentIntentView(APIView):
    """POST /api/payments/create-intent

    Body: { consultationId, fullName, contactNumber, email, seats?, ... }
    Creates a Stripe PaymentIntent (automatic payment methods: card + wallets)
    and a pending booking that reserves the seat. Amount is computed server-side.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        consultation = serializer.validated_data.get('consultation')
        if not consultation:
            raise ValidationError({'consultationId': 'This field is required.'})

        for field in ('full_name', 'contact_number', 'email'):
            if not serializer.validated_data.get(field):
                raise ValidationError({field: 'This field is required.'})

        booking_data = {
            key: value
            for key, value in serializer.validated_data.items()
            if key != 'consultation'
        }

        try:
            result = services.create_payment_intent(consultation, booking_data)
        except services.PaymentServiceError as exc:
            return Response(
                {
                    'success': False,
                    'error': {
                        'code': 'PAYMENT_INTENT_CREATE_FAILED',
                        'message': str(exc),
                        'details': {},
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(result, status=status.HTTP_201_CREATED)


@csrf_exempt
def stripe_webhook(request):
    """POST /api/payments/webhook — Stripe event delivery (authoritative confirm)."""
    if request.method != 'POST':
        return HttpResponse(status=405)

    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')

    if not settings.STRIPE_WEBHOOK_SECRET:
        logger.error('Stripe webhook secret is not configured.')
        return JsonResponse({'error': 'Webhook not configured'}, status=500)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError) as exc:
        logger.warning('Invalid Stripe signature: %s', exc)
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    try:
        services.handle_stripe_webhook_event(event)
    except Exception:
        logger.exception('Failed to process Stripe webhook event %s', event.get('type'))
        return JsonResponse({'error': 'Webhook handler error'}, status=500)

    return JsonResponse({'received': True}, status=200)
