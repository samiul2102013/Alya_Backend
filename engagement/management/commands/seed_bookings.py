from django.core.management.base import BaseCommand

from content.models import Consultation
from engagement.models import Booking


SESSIONS = [
    {
        'slug': 'premarital-communication',
        'session_title': 'Effective Communication for Couples',
        'session_type': 'counseling',
        'emirates': 'dubai',
        'date': '2026-09-12',
        'start_time': '10:00',
        'end_time': '12:00',
        'duration': '2 hours',
        'meeting_format': 'online',
        'session_link': 'https://meet.marage.ae/premarital-communication',
        'max_participants': 25,
        'fee': 120.00,
        'processing_fee': 5.00,
        'is_free': False,
        'counselor': 'Dr. Layla Haddad',
        'counselor_title': 'Licensed Family Counselor',
        'description': 'A practical workshop on healthy communication, conflict resolution and building trust before and during marriage.',
        'status': 'Published',
    },
    {
        'slug': 'financial-planning-2026',
        'session_title': 'Financial Planning for Newlyweds',
        'session_type': 'financial',
        'emirates': 'abudhabi',
        'date': '2026-09-20',
        'start_time': '14:00',
        'end_time': '16:00',
        'duration': '2 hours',
        'meeting_format': 'onsite',
        'max_participants': 40,
        'is_free': True,
        'counselor': 'Mr. Omar Al Mansoori',
        'counselor_title': 'Certified Financial Advisor',
        'description': 'Budgeting, savings, housing subsidies and financial planning tailored for newlywed Emirati couples.',
        'status': 'Published',
    },
    {
        'slug': 'legal-rights-marriage',
        'session_title': 'Marriage Legal Rights in the UAE',
        'session_type': 'legal',
        'emirates': 'sharjah',
        'date': '2026-10-01',
        'start_time': '11:00',
        'end_time': '13:00',
        'duration': '2 hours',
        'meeting_format': 'online',
        'session_link': 'https://meet.marage.ae/legal-rights',
        'max_participants': 30,
        'fee': 90.00,
        'processing_fee': 3.00,
        'is_free': False,
        'counselor': 'Adv. Fatima Al Zaabi',
        'counselor_title': 'Family Law Consultant',
        'description': 'Understanding marriage contracts, rights, responsibilities and legal documentation in the UAE.',
        'status': 'Published',
    },
    {
        'slug': 'family-health-nutrition',
        'session_title': 'Family Health & Nutrition Basics',
        'session_type': 'health',
        'emirates': 'ajman',
        'date': '2026-10-10',
        'start_time': '09:30',
        'end_time': '11:00',
        'duration': '1.5 hours',
        'meeting_format': 'onsite',
        'max_participants': 20,
        'is_free': True,
        'counselor': 'Dr. Hessa Mohammad',
        'counselor_title': 'Nutrition Specialist',
        'description': 'Practical nutrition and family wellness guidance for maintaining a healthy household.',
        'status': 'Published',
    },
]

BOOKINGS = [
    {
        'session_ref': 'premarital-communication',
        'full_name': 'Ahmed Al Ali',
        'contact_number': '+971 50 123 4567',
        'email': 'ahmed.alali@example.com',
        'user_type': 'individual',
        'seats': 2,
        'payment_method': 'card',
        'status': 'confirmed',
        'notes': 'Couple attending together. Prefer English session.',
    },
    {
        'session_ref': 'premarital-communication',
        'full_name': 'Mariam Khalifa',
        'contact_number': '+971 52 234 5678',
        'email': 'mariam.khalifa@example.com',
        'user_type': 'individual',
        'seats': 1,
        'payment_method': 'apple_pay',
        'status': 'confirmed',
        'notes': '',
    },
    {
        'session_ref': 'premarital-communication',
        'full_name': 'Rashid Al Mazrouei',
        'contact_number': '+971 55 345 6789',
        'email': 'rashid.m@example.com',
        'user_type': 'individual',
        'seats': 2,
        'payment_method': 'card',
        'status': 'pending_payment',
        'notes': 'Waiting to receive payment link.',
    },
    {
        'session_ref': 'financial-planning-2026',
        'full_name': 'Nouf Al Suwaidi',
        'contact_number': '+971 56 456 7890',
        'email': 'nouf.suwaidi@example.com',
        'user_type': 'couple',
        'seats': 1,
        'payment_method': 'card',
        'status': 'confirmed',
        'notes': 'Asked about Abu Dhabi housing subsidy forms.',
    },
    {
        'session_ref': 'financial-planning-2026',
        'full_name': 'Khalid Al Habtoor',
        'contact_number': '+971 50 567 8901',
        'email': 'khalid.h@example.com',
        'user_type': 'organization',
        'company_or_organization': 'Marriage Support Center - Abu Dhabi',
        'seats': 8,
        'payment_method': 'card',
        'status': 'confirmed',
        'notes': 'Booking a corporate block for center clients.',
    },
    {
        'session_ref': 'legal-rights-marriage',
        'full_name': 'Sara Al Hashimi',
        'contact_number': '+971 54 678 9012',
        'email': 'sara.hashimi@example.com',
        'user_type': 'individual',
        'seats': 1,
        'payment_method': 'apple_pay',
        'status': 'confirmed',
        'notes': '',
    },
    {
        'session_ref': 'legal-rights-marriage',
        'full_name': 'Youssef Benali',
        'contact_number': '+971 58 789 0123',
        'email': 'youssef.benali@example.com',
        'user_type': 'couple',
        'seats': 2,
        'payment_method': 'card',
        'status': 'cancelled',
        'notes': 'Booked by mistake, requested cancellation.',
    },
    {
        'session_ref': 'family-health-nutrition',
        'full_name': 'Aisha Al Qassemi',
        'contact_number': '+971 52 890 1234',
        'email': 'aisha.qassemi@example.com',
        'user_type': 'individual',
        'seats': 1,
        'payment_method': 'card',
        'status': 'confirmed',
        'notes': '',
    },
]


def booking_amount(consultation, seats=1):
    """Mirror the public booking flow cost calc: (fee + processing_fee - discount) * seats."""
    if consultation.is_free:
        return 0
    unit = max(consultation.fee or 0, 0) + max(consultation.processing_fee or 0, 0) - max(consultation.discount or 0, 0)
    return round(max(unit, 0) * int(seats), 2)


class Command(BaseCommand):
    help = 'Seed consultation sessions and bookings for testing the admin Booked Consultations tab.'

    def handle(self, *args, **options):
        created_sessions = []

        for data in SESSIONS:
            consultation, created = Consultation.objects.get_or_create(
                slug=data['slug'],
                defaults=data,
            )
            if created:
                created_sessions.append(consultation.session_title)
                self.stdout.write(self.style.SUCCESS(f'Created session: {consultation.session_title}'))
            else:
                self.stdout.write(f'Session already exists: {consultation.session_title}')

        if not created_sessions:
            self.stdout.write(self.style.WARNING('No new sessions created; using existing sessions for bookings.'))

        sessions = {c.slug: c for c in Consultation.objects.all()}
        created_bookings = 0
        for b in BOOKINGS:
            consultation = sessions.get(b['session_ref'])
            if consultation is None:
                self.stdout.write(self.style.WARNING(f"Skipping booking for missing session slug: {b['session_ref']}"))
                continue

            defaults = {
                'consultation': consultation,
                'full_name': b['full_name'],
                'contact_number': b['contact_number'],
                'email': b['email'],
                'user_type': b.get('user_type', 'individual'),
                'company_or_organization': b.get('company_or_organization', ''),
                'seats': b.get('seats', 1),
                'status': b['status'],
                'payment_method': b.get('payment_method', 'card'),
                'notes': b.get('notes', ''),
                'amount': booking_amount(consultation, b.get('seats', 1)),
                'payment_success': b['status'] == 'confirmed',
            }

            # Idempotent upsert keyed on (email, session).
            booking, created = Booking.objects.get_or_create(
                email=b['email'],
                consultation_id=consultation.pk,
                defaults=defaults,
            )
            if created:
                created_bookings += 1
                self.stdout.write(self.style.SUCCESS(f'Created booking: {booking.reference} - {booking.full_name}'))
            else:
                self.stdout.write(f'Booking already exists: {booking.reference}')

        self.stdout.write(self.style.SUCCESS(
            f'Seeding complete. {created_bookings} new booking(s) of {len(BOOKINGS)} total in list.'
        ))
