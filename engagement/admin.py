from django.contrib import admin

from .models import Booking, ContactMessage, InitiativeApplication


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('reference', 'full_name', 'email', 'consultation', 'status', 'created_at')
    search_fields = ('reference', 'full_name', 'email')
    list_filter = ('status',)


@admin.register(InitiativeApplication)
class InitiativeApplicationAdmin(admin.ModelAdmin):
    list_display = ('application_reference', 'full_name', 'email', 'initiative', 'status')
    search_fields = ('application_reference', 'full_name', 'email')
    list_filter = ('status',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')