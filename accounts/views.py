from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from .models import PrivacyPolicy, Terms
from .serializers import (
    AdminUserSerializer,
    ChangePasswordSerializer,
    LoginSerializer,
    PrivacyPolicySerializer,
    ProfileSerializer,
    TermsSerializer,
)


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception:
            pass
        return Response({'success': True})


class SettingsView(APIView):
    """GET /admin/settings"""

    def get(self, request):
        privacy = PrivacyPolicy.objects.first() or PrivacyPolicy.objects.create()
        terms = Terms.objects.first() or Terms.objects.create()
        return Response({
            'profile': AdminUserSerializer(request.user).data,
            'privacy_policy': PrivacyPolicySerializer(privacy).data,
            'terms': TermsSerializer(terms).data,
        })


class ProfileView(APIView):
    """PUT /admin/settings/profile"""

    def put(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(AdminUserSerializer(request.user).data)


class ChangePasswordView(APIView):
    """POST /admin/settings/change-password"""

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data['current_password']):
            return Response(
                {
                    'success': False,
                    'error': {
                        'code': 'INVALID_PASSWORD',
                        'message': 'Current password is incorrect',
                        'details': {'current_password': ['Current password is incorrect']},
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'success': True})


class PrivacyPolicyView(APIView):
    """PUT /admin/settings/privacy"""

    def put(self, request):
        instance = PrivacyPolicy.objects.first() or PrivacyPolicy.objects.create()
        serializer = PrivacyPolicySerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': True})


class TermsView(APIView):
    """PUT /admin/settings/terms"""

    def put(self, request):
        instance = Terms.objects.first() or Terms.objects.create()
        serializer = TermsSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': True})


class PublicPrivacyPolicyView(APIView):
    """GET /api/privacy — public privacy policy content for the user panel."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        instance = PrivacyPolicy.objects.first() or PrivacyPolicy.objects.create()
        return Response(PrivacyPolicySerializer(instance).data)


class PublicTermsView(APIView):
    """GET /api/terms — public terms & conditions content for the user panel."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        instance = Terms.objects.first() or Terms.objects.create()
        return Response(TermsSerializer(instance).data)