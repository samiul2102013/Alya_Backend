from django.core.management.base import BaseCommand
from content.models import DEFAULT_FOOTER_CONTENT, FooterContent


class Command(BaseCommand):
    help = 'Seed FooterContent with default EN/AR content from translations.'

    def handle(self, *args, **options):
        self.stdout.write('Seeding FooterContent defaults...')

        obj, created = FooterContent.objects.update_or_create(
            pk=FooterContent.objects.first().pk if FooterContent.objects.exists() else None,
            defaults=DEFAULT_FOOTER_CONTENT,
        )

        action = 'Created' if created else 'Updated'
        self.stdout.write(self.style.SUCCESS(f'{action} FooterContent (pk={obj.pk}) with {len(DEFAULT_FOOTER_CONTENT)} fields.'))
