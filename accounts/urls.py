from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path('auth/login/', views.LoginView.as_view(), name='admin-login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='admin-refresh'),
    path('auth/logout/', views.LogoutView.as_view(), name='admin-logout'),
    path('settings/', views.SettingsView.as_view(), name='admin-settings'),
    path('settings/profile/', views.ProfileView.as_view(), name='admin-settings-profile'),
    path('settings/change-password/', views.ChangePasswordView.as_view(), name='admin-settings-password'),
    path('settings/privacy/', views.PrivacyPolicyView.as_view(), name='admin-settings-privacy'),
    path('settings/terms/', views.TermsView.as_view(), name='admin-settings-terms'),
]