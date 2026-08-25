from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ApplicationAdminViewSet,
    BookingAdminViewSet,
    BookingCreateView,
    BookingLookupView,
    ContactCreateView,
    InitiativeApplicationCreateView,
)

router = DefaultRouter(trailing_slash=False)
router.register(r'admin/bookings', BookingAdminViewSet, basename='admin-bookings')
router.register(r'admin/applications', ApplicationAdminViewSet, basename='admin-applications')

urlpatterns = [
    path('consultations/book', BookingCreateView.as_view(), name='consultations-book'),
    path('consultations/bookings/<str:reference>', BookingLookupView.as_view(), name='consultations-booking-lookup'),
    path('initiatives/<str:initiative_id>/apply/', InitiativeApplicationCreateView.as_view(), name='initiatives-apply'),
    path('contact/', ContactCreateView.as_view(), name='contact'),
] + router.urls