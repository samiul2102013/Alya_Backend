from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import AdminUserManager


class AdminUser(AbstractBaseUser, PermissionsMixin):
    """Custom admin user used by the admin dashboard (JWT + Bearer token)."""

    name = models.CharField('Name', max_length=255, blank=True)
    username = models.CharField('Username', max_length=150, unique=True, blank=True)
    email = models.EmailField('Email', max_length=255, unique=True)
    contact_number = models.CharField('Contact Number', max_length=30, blank=True)

    is_admin_user = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = AdminUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Admin User'
        verbose_name_plural = 'Admin Users'

    def __str__(self):
        return self.name or self.email


class PrivacyPolicy(models.Model):
    """Singleton holding the privacy policy rich HTML content."""

    content = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Privacy Policy'
        verbose_name_plural = 'Privacy Policies'

    def __str__(self):
        return f'Privacy Policy ({self.updated_at:%Y-%m-%d})'


class Terms(models.Model):
    """Singleton holding the terms & conditions rich HTML content."""

    content = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Terms'
        verbose_name_plural = 'Terms'

    def __str__(self):
        return f'Terms ({self.updated_at:%Y-%m-%d})'