import uuid

from django.db import models

from content.enums import BookingStatus, PaymentMethod, UserType
from content.models import Consultation, Initiative


class TimeStampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Booking(TimeStampedModel):
    """Session booking (API spec 3.3)."""

    reference = models.CharField('Reference', max_length=20, unique=True, blank=True)
    consultation = models.ForeignKey(
        Consultation, on_delete=models.CASCADE, related_name='bookings'
    )

    full_name = models.CharField('Full Name', max_length=200)
    contact_number = models.CharField('Contact Number', max_length=30)
    email = models.EmailField('Email')

    user_type = models.CharField('User Type', max_length=20, choices=UserType.choices, default=UserType.INDIVIDUAL)
    company_or_organization = models.CharField('Company / Organization', max_length=200, blank=True)

    seats = models.PositiveIntegerField('Seats', default=1)
    session_date = models.DateField('Session Date', null=True, blank=True)
    session_snapshot = models.JSONField('Session Snapshot', default=dict, blank=True)
    notes = models.TextField('Notes', blank=True)

    payment_method = models.CharField('Payment Method', max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CARD)
    amount = models.DecimalField('Amount', max_digits=10, decimal_places=2, default=0)
    payment_reference = models.CharField('Payment Reference', max_length=100, blank=True)
    payment_success = models.BooleanField('Payment Success', default=False)

    status = models.CharField('Status', max_length=20, choices=BookingStatus.choices, default=BookingStatus.PENDING_PAYMENT)

    # For paid bookings: the deadline by which payment must complete before the
    # scheduled job cancels the booking and releases the seat.
    expires_at = models.DateTimeField('Expires At', null=True, blank=True)

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = f'BK-{self._gen_id()}'
        # Record the session data at booking time (price + schedule frozen).
        if not self.session_snapshot:
            self.session_snapshot = self._build_session_snapshot()
        super().save(*args, **kwargs)

    @staticmethod
    def _gen_id():
        return uuid.uuid4().hex[:8].upper()

    def _build_session_snapshot(self):
        c = self.consultation
        return {
            'sessionTitle': c.session_title,
            'sessionType': c.session_type,
            'date': c.date.isoformat() if c.date else None,
            'startTime': c.start_time,
            'endTime': c.end_time,
            'duration': c.duration,
            'timeZone': c.time_zone,
            'meetingFormat': c.meeting_format,
            'location': c.counselor_title,
            'counselor': c.counselor,
        }

    def __str__(self):
        return self.reference or self.full_name


class InitiativeApplication(TimeStampedModel):
    """Initiative application (API spec 3.1)."""

    application_reference = models.CharField('Reference', max_length=20, unique=True, blank=True)
    initiative = models.ForeignKey(
        Initiative, on_delete=models.CASCADE, related_name='applications'
    )

    full_name = models.CharField('Full Name', max_length=200)
    contact_number = models.CharField('Contact Number', max_length=30)
    email = models.EmailField('Email')

    user_type = models.CharField('User Type', max_length=20, choices=UserType.choices, default=UserType.INDIVIDUAL)
    user_or_organization_name = models.CharField('User / Organization Name', max_length=200, blank=True)

    marital_status = models.CharField('Marital Status', max_length=30, blank=True)
    age = models.PositiveIntegerField('Age', null=True, blank=True)
    emirate = models.CharField('Emirate', max_length=30, blank=True)
    income = models.CharField('Income', max_length=100, blank=True)
    family_members = models.PositiveIntegerField('Family Members', default=0)
    nationality = models.CharField('Nationality', max_length=100, blank=True)
    notes = models.TextField('Notes', blank=True)

    status = models.CharField(
        'Status',
        max_length=20,
        choices=[
            ('received', 'Received'),
            ('reviewing', 'Reviewing'),
            ('shortlisted', 'Shortlisted'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
        ],
        default='received',
    )

    class Meta:
        verbose_name = 'Initiative Application'
        verbose_name_plural = 'Initiative Applications'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.application_reference:
            self.application_reference = f'APP-{uuid.uuid4().hex[:8].upper()}'
        super().save(*args, **kwargs)


class ContactMessage(TimeStampedModel):
    """Contact form submission (API spec 3.4)."""

    name = models.CharField('Name', max_length=200)
    email = models.EmailField('Email')
    phone = models.CharField('Phone', max_length=30, blank=True)
    subject = models.CharField('Subject', max_length=300, blank=True)
    message = models.TextField('Message')

    class Meta:
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name}: {self.subject}'