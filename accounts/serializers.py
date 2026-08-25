from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import AdminUser, PrivacyPolicy, Terms


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = ['id', 'name', 'username', 'email', 'contact_number']
        read_only_fields = ['id']


class LoginSerializer(TokenObtainPairSerializer):
    """Token login using email + password; returns access, refresh, user."""

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = AdminUserSerializer(self.user).data
        return data


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = ['username', 'email', 'contact_number']

    def validate_email(self, value):
        qs = AdminUser.objects.filter(email__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('Email is already in use')
        return value

    def validate_username(self, value):
        qs = AdminUser.objects.filter(username__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('Username is already in use')
        return value


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'new_password': 'Passwords do not match'})
        if attrs['current_password'] == attrs['new_password']:
            raise serializers.ValidationError({'new_password': 'New password must differ from current password'})
        return attrs


class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = ['content', 'updated_at']
        read_only_fields = ['updated_at']


class TermsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terms
        fields = ['content', 'updated_at']
        read_only_fields = ['updated_at']