from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from django.db.models import Q

from content.models import Consultation
from content.enums import BookingStatus
from payments import services

from .models import Booking, ContactMessage, InitiativeApplication
from .serializers import (
    BookingAdminSerializer,
    BookingSerializer,
    ContactSerializer,
    InitiativeApplicationSerializer,
)


def booking_ref():
    return Booking._gen_id()


def _not_session_available():
    return PermissionDenied('This consultation session is not available for booking.')


class BookingCreateView(APIView):
    """POST /api/consultations/book — confirm a consultation booking.

    Two flows:
    * Paid sessions — the client first calls ``/api/payments/create-intent``,
      receives a ``paymentIntentId``, and submits it here. The PaymentIntent is
      verified server-side with Stripe before the booking is marked CONFIRMED.
      Idempotent: an already-confirmed booking returns success without
      double-processing.
    * Free / zero-cost sessions — submitted directly with the booking fields,
      confirmed immediately (unchanged no-payment path).
    """

    permission_classes = [AllowAny]

    def post(self, request):
        payment_intent_id = request.data.get('paymentIntentId')

        if payment_intent_id:
            try:
                booking = services.confirm_booking_payment(payment_intent_id)
            except services.PaymentServiceError as exc:
                return Response(
                    {
                        'success': False,
                        'error': {
                            'code': 'PAYMENT_VERIFICATION_FAILED',
                            'message': str(exc),
                            'details': {},
                        },
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(BookingSerializer(booking).data, status=201)

        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        consultation = serializer.validated_data.get('consultation')
        if not consultation:
            return Response(
                {
                    'success': False,
                    'error': {
                        'code': 'CONSULTATION_REQUIRED',
                        'message': 'A consultation is required',
                        'details': {'consultationId': ['This field is required.']},
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if consultation.status != 'Published' or not consultation.is_bookable:
            raise _not_session_available()

        seats = serializer.validated_data.get('seats', 1) or 1
        seats_left = consultation.seats_left
        if seats_left is not None and seats > max(seats_left, 0):
            return Response(
                {
                    'success': False,
                    'error': {
                        'code': 'NO_SEATS',
                        'message': 'Not enough seats available for this session.',
                        'details': {'seats': [f'Only {seats_left} seat(s) left.']},
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        amount = 0
        if not consultation.is_free:
            amount = (consultation.fee or 0) + (consultation.processing_fee or 0) - (consultation.discount or 0)
            amount = max(amount, 0)

        booking = serializer.save(
            status=BookingStatus.CONFIRMED,
            amount=amount,
            payment_success=True,
            payment_reference=f'PY-{booking_ref()}',
        )
        return Response(BookingSerializer(booking).data, status=201)


class BookingLookupView(APIView):
    """GET /api/consultations/bookings/<reference> — public confirmation lookup by reference."""

    permission_classes = [AllowAny]

    def get(self, request, reference):
        booking = Booking.objects.filter(reference__iexact=reference).first()
        if not booking:
            raise NotFound('Booking not found.')
        return Response(BookingSerializer(booking).data)


class InitiativeApplicationCreateView(APIView):
    """POST /api/initiatives/:id/apply — public application submission."""

    permission_classes = [AllowAny]

    def post(self, request, initiative_id):
        data = dict(request.data)
        data['initiativeId'] = initiative_id
        serializer = InitiativeApplicationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        application = serializer.save(status='received')
        return Response(InitiativeApplicationSerializer(application).data, status=201)


class ContactCreateView(APIView):
    """POST /api/contact — contact form."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        return Response(ContactSerializer(message).data, status=201)


class BookingAdminViewSet(ModelViewSet):
    """GET/PUT /api/admin/bookings - list, retrieve, partial update status."""

    http_method_names = ['get', 'put', 'patch', 'head', 'options']
    queryset = Booking.objects.all().order_by('-created_at')
    serializer_class = BookingAdminSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search')
        status_filter = self.request.query_params.get('status')
        if search:
            qs = qs.filter(
                Q(full_name__icontains=search)
                | Q(email__icontains=search)
                | Q(contact_number__icontains=search)
                | Q(reference__icontains=search)
                | Q(consultation__session_title__icontains=search)
            )
        if status_filter:
            qs = qs.filter(status__iexact=status_filter)
        return qs


class ApplicationAdminViewSet(ModelViewSet):
    """GET/PUT /api/admin/applications — list, retrieve, partial update status."""

    http_method_names = ['get', 'put', 'patch', 'head', 'options']
    queryset = InitiativeApplication.objects.all().order_by('-created_at')
    serializer_class = InitiativeApplicationSerializer
    lookup_field = 'pk'