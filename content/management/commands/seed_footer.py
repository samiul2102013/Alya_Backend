from django.core.management.base import BaseCommand
from content.models import FooterContent


class Command(BaseCommand):
    help = 'Seed FooterContent with default EN/AR content from translations.'

    def handle(self, *args, **options):
        self.stdout.write('Seeding FooterContent defaults...')

        data = {
            'brand_text': 'Alia is the official platform dedicated to empowering Emirati families through comprehensive marriage guidance, financial grants, and lifelong community support.',
            'brand_text_ar': 'عالية هي المنصة الرسمية المكرسة لتمكين الأسر الإماراتية من خلال إرشادات الزواج الشاملة والمنح المالية والدعم المجتمعي مدى الحياة.',
            'government_label': 'United Arab Emirates Government Initiative',
            'government_label_ar': 'مبادرة حكومة دولة الإمارات العربية المتحدة',

            'quick_links': [
                {'label': 'Home', 'labelAr': 'الرئيسية', 'href': '/'},
                {'label': 'About Alia', 'labelAr': 'عن عالية', 'href': '/about'},
                {'label': 'Contact Us', 'labelAr': 'اتصل بنا', 'href': '/contact'},
                {'label': 'National Initiatives', 'labelAr': 'المبادرات الوطنية', 'href': '/initiatives'},
                {'label': 'Emirates Centers', 'labelAr': 'مراكز الإمارات', 'href': '/emirates'},
                {'label': 'Privacy Policy', 'labelAr': 'سياسة الخصوصية', 'href': '/privacy-policy'},
                {'label': 'Terms & Conditions', 'labelAr': 'الشروط والأحكام', 'href': '/terms-and-conditions'},
            ],
            'resource_links': [
                {'label': 'Wedding Grants FAQ', 'labelAr': 'الأسئلة الشائعة لمنح الزواج', 'href': '#'},
                {'label': 'UAE Family Law Guide', 'labelAr': 'دليل قانون الأسرة في الإمارات', 'href': '#'},
                {'label': 'Housing Subsidy Portal', 'labelAr': 'بوابة دعم السكن', 'href': '#'},
                {'label': 'Media Center & News', 'labelAr': 'مركز الإعلام والأخبار', 'href': '/news'},
            ],

            'phone': '+971 800 2542',
            'email': 'support@alia.gov.ae',
            'address': 'Abu Dhabi, UAE',
            'address_ar': 'أبوظبي، الإمارات العربية المتحدة',

            'copyright_text': 'All rights reserved.',
            'copyright_text_ar': 'جميع الحقوق محفوظة.',
            'built_for_text': 'Built for Emirati Families',
            'built_for_text_ar': 'صُمم من أجل الأسر الإماراتية',

            'published': True,
        }

        obj, created = FooterContent.objects.update_or_create(
            pk=FooterContent.objects.first().pk if FooterContent.objects.exists() else None,
            defaults=data,
        )

        action = 'Created' if created else 'Updated'
        self.stdout.write(self.style.SUCCESS(f'{action} FooterContent (pk={obj.pk}) with {len(data)} fields.'))
