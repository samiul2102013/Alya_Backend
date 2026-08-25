from rest_framework import serializers

from content.models import Consultation, Initiative

from .models import Booking, ContactMessage, InitiativeApplication


class BookingSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='pk', read_only=True)
    consultationId = serializers.PrimaryKeyRelatedField(
        source='consultation', queryset=Consultation.objects.all(), required=False
    )
    fullName = serializers.CharField(source='full_name', required=False)
    contactNumber = serializers.CharField(source='contact_number', required=False)
    userType = serializers.CharField(source='user_type', required=False, allow_blank=True)
    companyOrOrganization = serializers.CharField(source='company_or_organization', required=False, allow_blank=True)
    sessionDate = serializers.DateField(source='session_date', required=False)
    sessionSnapshot = serializers.JSONField(source='session_snapshot', read_only=True)
    paymentMethod = serializers.CharField(source='payment_method', required=False, allow_blank=True)
    paymentReference = serializers.CharField(source='payment_reference', required=False, allow_blank=True)
    paymentSuccess = serializers.BooleanField(source='payment_success', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'reference', 'consultationId', 'fullName', 'contactNumber', 'email',
                  'userType', 'companyOrOrganization', 'seats', 'sessionDate', 'sessionSnapshot',
                  'notes', 'paymentMethod', 'amount', 'paymentReference', 'paymentSuccess', 'status',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'reference', 'sessionSnapshot', 'paymentSuccess', 'status', 'created_at', 'updated_at']


class BookingAdminSerializer(BookingSerializer):
    class Meta(BookingSerializer.Meta):
        read_only_fields = ['id', 'reference', 'sessionSnapshot', 'paymentSuccess', 'created_at', 'updated_at']


class InitiativeApplicationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='pk', read_only=True)
    applicationReference = serializers.CharField(source='application_reference', read_only=True)
    initiativeId = serializers.PrimaryKeyRelatedField(
        source='initiative', queryset=Initiative.objects.all(), required=False
    )
    fullName = serializers.CharField(source='full_name', required=False, allow_blank=True)
    contactNumber = serializers.CharField(source='contact_number', required=False, allow_blank=True)
    userType = serializers.CharField(source='user_type', required=False, allow_blank=True)
    userOrOrganizationName = serializers.CharField(source='user_or_organization_name', required=False, allow_blank=True)
    maritalStatus = serializers.CharField(source='marital_status', required=False, allow_blank=True)
    familyMembers = serializers.IntegerField(source='family_members', required=False)
    emirate = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = InitiativeApplication
        fields = ['id', 'applicationReference', 'initiativeId', 'fullName', 'contactNumber', 'email',
                  'userType', 'userOrOrganizationName', 'maritalStatus', 'age', 'emirate', 'income',
                  'familyMembers', 'nationality', 'notes', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'applicationReference', 'created_at', 'updated_at']


class ContactSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='pk', read_only=True)

    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'phone', 'subject', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']