from django.core.management.base import BaseCommand
from content.models import ContactContent


class Command(BaseCommand):
    help = 'Seed ContactContent with default EN/AR content from translations.'

    def handle(self, *args, **options):
        self.stdout.write('Seeding ContactContent defaults...')

        data = {
            'title': 'Get in Touch — We Are Here to Support You',
            'title_ar': 'تواصل معنا — نحن هنا لدعمك',
            'description': 'Have questions about marriage support programs, consultation services, or community initiatives?',
            'description_ar': 'هل لديك أسئلة حول برامج دعم الزواج أو خدمات الاستشارات أو المبادرات المجتمعية؟',
            'browse_session': 'Browse Session',
            'browse_session_ar': 'تصفح الجلسة',
            'contact_support': 'Contact Support',
            'contact_support_ar': 'تواصل مع الدعم',

            'send_message': 'Send us a message',
            'send_message_ar': 'أرسل لنا رسالة',
            'send_message_sub': 'Tell us how can we assist you today?',
            'send_message_sub_ar': 'أخبرنا كيف يمكننا مساعدتك اليوم؟',
            'full_name': 'Full Name',
            'full_name_ar': 'الاسم الكامل',
            'full_name_placeholder': 'Enter your full name',
            'full_name_placeholder_ar': 'أدخل اسمك الكامل',
            'email_label': 'Email',
            'email_label_ar': 'البريد الإلكتروني',
            'email_placeholder': 'Enter your email',
            'email_placeholder_ar': 'أدخل بريدك الإلكتروني',
            'user_type': 'User Type',
            'user_type_ar': 'نوع المستخدم',
            'select_user_type': 'Select user type',
            'select_user_type_ar': 'اختر نوع المستخدم',
            'individual': 'Individual',
            'individual_ar': 'فرد',
            'couple': 'Couple',
            'couple_ar': 'زوجان',
            'organization': 'Organization',
            'organization_ar': 'منظمة',
            'subject_label': 'Subject',
            'subject_label_ar': 'الموضوع',
            'subject_placeholder': 'Enter subject',
            'subject_placeholder_ar': 'أدخل الموضوع',
            'phone_label': 'Phone Number',
            'phone_label_ar': 'رقم الهاتف',
            'phone_placeholder': 'Enter your phone number',
            'phone_placeholder_ar': 'أدخل رقم هاتفك',
            'message_label': 'Your Message',
            'message_label_ar': 'رسالتك',
            'message_placeholder': 'Write your message here...',
            'message_placeholder_ar': 'اكتب رسالتك هنا...',
            'send_button': 'Send Message',
            'send_button_ar': 'إرسال الرسالة',
            'success_message': 'Your message has been sent successfully. We\'ll get back to you soon.',
            'success_message_ar': 'تم إرسال رسالتك بنجاح. سنتواصل معك قريباً.',
            'sending': 'Sending...',
            'sending_ar': 'جاري الإرسال...',

            'contact_info': 'Contact Information',
            'contact_info_ar': 'معلومات الاتصال',
            'office_address': 'Office Address',
            'office_address_ar': 'عنوان المكتب',
            'working_hours': 'Working Hours',
            'working_hours_ar': 'ساعات العمل',
            'general_inquiries': 'General Inquiries',
            'general_inquiries_ar': 'استفسارات عامة',
            'support_heading': 'Support',
            'support_heading_ar': 'الدعم',
            'address_lines': ['Dubai, United Arab Emirates', 'info@marage.ae', '+971 50 123 4567'],
            'address_lines_ar': ['دبي، الإمارات العربية المتحدة', 'info@marage.ae', '+971 50 123 4567'],
            'hours_lines': ['Mon – Fri: 9:00 AM – 6:00 PM', 'Saturday: 10:00 AM – 2:00 PM', 'Sunday: Closed'],
            'hours_lines_ar': ['الإثنين – الجمعة: 9:00 صباحاً – 6:00 مساءً', 'السبت: 10:00 صباحاً – 2:00 ظهراً', 'الأحد: مغلق'],
            'inquiries_lines': ['Email: info@marage.ae', 'Phone: +971 50 123 4567'],
            'inquiries_lines_ar': ['البريد الإلكتروني: info@marage.ae', 'الهاتف: +971 50 123 4567'],
            'support_lines': ['Email: support@marage.ae', 'Phone: +971 50 987 6543'],
            'support_lines_ar': ['البريد الإلكتروني: support@marage.ae', 'الهاتف: +971 50 987 6543'],

            'our_location': 'Our Location',
            'our_location_ar': 'موقعنا',
            'our_location_text': 'Visit us at our main office in Dubai, UAE.',
            'our_location_text_ar': 'زورنا في مكتبنا الرئيسي في دبي، الإمارات.',
            'map_title': 'Alia Office Location',
            'map_title_ar': 'موقع مكتب عالية',
            'map_embed_url': '',
            'latitude': '25.2048',
            'longitude': '55.2708',

            'published': True,
        }

        obj, created = ContactContent.objects.update_or_create(
            pk=ContactContent.objects.first().pk if ContactContent.objects.exists() else None,
            defaults=data,
        )

        action = 'Created' if created else 'Updated'
        self.stdout.write(self.style.SUCCESS(f'{action} ContactContent (pk={obj.pk}) with {len(data)} fields.'))
