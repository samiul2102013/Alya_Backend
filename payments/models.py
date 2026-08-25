import uuid

from django.db import models


class PaymentStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    SUCCEEDED = 'succeeded', 'Succeeded'
    FAILED = 'failed', 'Failed'
    CANCELED = 'canceled', 'Canceled'


class Payment(models.Model):
    """A Stripe PaymentIntent linked to a consultation booking.

    The intent is created before payment is collected, so the FK to Booking is
    set at creation time (the booking is created as ``pending_payment`` to
    reserve the seat). ``status`` mirrors the Stripe PaymentIntent state.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.OneToOneField(
        'engagement.Booking',
        on_delete=models.CASCADE,
        related_name='payment',
        null=True,
        blank=True,
    )

    stripe_payment_intent_id = models.CharField('Stripe PaymentIntent ID', max_length=100, unique=True)
    client_secret = models.CharField('Client Secret', max_length=255)
    amount = models.DecimalField('Amount', max_digits=10, decimal_places=2, default=0)
    currency = models.CharField('Currency', max_length=3, default='aed')

    status = models.CharField(
        'Status', max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-created_at']

    def __str__(self):
        return self.stripe_payment_intent_id
