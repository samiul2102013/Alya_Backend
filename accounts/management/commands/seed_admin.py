import os

from django.core.management.base import BaseCommand

from accounts.models import AdminUser


class Command(BaseCommand):
    help = 'Create (or update) the admin/superuser from environment variables.'

    def handle(self, *args, **options):
        email = os.environ.get('ADMIN_EMAIL') or os.environ.get('SEED_ADMIN_EMAIL')
        username = os.environ.get('ADMIN_USERNAME') or os.environ.get('SEED_ADMIN_USERNAME')
        password = os.environ.get('ADMIN_PASSWORD') or os.environ.get('SEED_ADMIN_PASSWORD')
        name = os.environ.get('ADMIN_NAME') or os.environ.get('SEED_ADMIN_NAME') or 'Admin'

        if not email or not password:
            self.stdout.write(
                self.style.WARNING(
                    'ADMIN_EMAIL/ADMIN_PASSWORD not set. Skipping admin creation.'
                )
            )
            return

        user, created = AdminUser.objects.get_or_create(
            email__iexact=email,
            defaults={'email': email, 'username': username or email.split('@')[0],
                      'name': name, 'is_staff': True, 'is_superuser': True,
                      'is_admin_user': True},
        )

        if not created:
            user.email = email
            user.username = username or user.username
            user.name = name
            user.is_staff = True
            user.is_superuser = True
            user.is_admin_user = True

        user.set_password(password)
        user.save()
        self.stdout.write(
            self.style.SUCCESS(f'Admin ready: {email} ({"created" if created else "updated"})')
        )