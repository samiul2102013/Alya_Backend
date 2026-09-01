from django.core.management.base import BaseCommand
from content.models import AboutContent


class Command(BaseCommand):
    help = 'Seed AboutContent with default EN/AR content from translations.'

    def handle(self, *args, **options):
        self.stdout.write('Seeding AboutContent defaults...')

        data = {
            'title': 'About Alia - Supporting Stronger Families Across the UAE',
            'title_ar': 'عن عالية - دعم أسراً أقوى في جميع أنحاء الإمارات',
            'description': 'Alia is the official UAE platform dedicated to empowering Emirati families through trusted marriage guidance, government programs, expert consultation sessions, and community-driven initiatives.',
            'description_ar': 'عالية هي المنصة الرسمية الإماراتية المكرسة لتمكين الأسر الإماراتية من خلال إرشادات الزواج الموثوقة والبرامج الحكومية وجلسات الاستشارات المتخصصة والمبادرات المجتمعية.',
            'browse_session': 'Browse Session',
            'browse_session_ar': 'تصفح الجلسة',
            'contact_support': 'Contact Support',
            'contact_support_ar': 'تواصل مع الدعم',

            'our_story': 'Our Story',
            'our_story_ar': 'قصتنا',
            'our_story_text': 'Alia was created to serve as the centralized platform for marriage support services across the UAE.',
            'our_story_text_ar': 'تم إنشاء عالية لتكون المنصة المركزة لخدمات دعم الزواج في جميع أنحاء الإمارات.',

            'our_mission': 'Our Mission',
            'our_mission_ar': 'مهمتنا',
            'our_mission_text': 'Provide easy access to trusted marriage support services, resources, and expert guidance.',
            'our_mission_text_ar': 'توفير سهل الوصول إلى خدمات دعم الزواج الموثوقة والموارد والإرشادات المتخصصة.',

            'our_vision': 'Our Vision',
            'our_vision_ar': 'رؤيتنا',
            'our_vision_text': 'A UAE where every marriage is supported, every family is empowered.',
            'our_vision_text_ar': 'إمارات حيث كل زواج مدعوم، وكل أسرة ممكّنة.',

            'our_objective': 'Our Objective',
            'our_objective_ar': 'أهدافنا',
            'our_objective_text': 'Our objective is to focus on making trusted marriage support services more accessible.',
            'our_objective_text_ar': 'هدفنا هو التركيز على جعل خدمات دعم الزواج الموثوقة أكثر سهولة في الوصول.',
            'objectives': [
                'Promote Healthy Marriage',
                'Connect Users with Trusted Initiatives',
                'Improve Access to Consultation Service',
                'Support Families\' Well-being',
                'Increase Awareness of Available Programs',
                'Encourage Lifelong Learning',
            ],

            'what_we_offer': 'What We Offer',
            'what_we_offer_ar': 'ما نقدمه',
            'what_we_offer_text': 'Access trusted resources, expert consultations, educational content, and community support services.',
            'what_we_offer_text_ar': 'الوصول إلى موارد موثوقة واستشارات متخصصة ومحتوى تعليمي وخدمات دعم مجتمعية.',
            'offerings': [
                {'title': 'Marriage Initiative', 'titleAr': 'مبادرة الزواج', 'desc': 'Explore verified government and private programs.', 'descAr': 'استكشف البرامج الحكومية والخاصة المعتمدة.'},
                {'title': 'Consultation Sessions', 'titleAr': 'جلسات الاستشارة', 'desc': 'Connect with professional counselors and marriage experts.', 'descAr': 'تواصل مع المستشارين المحترفين وخبراء الزواج.'},
                {'title': 'Educational Shorts', 'titleAr': 'مقاطع تعليمية', 'desc': 'Watch informative videos covering marriage preparation.', 'descAr': 'شاهد مقاطع فيديو تعليمية تغطي التحضير للزواج.'},
                {'title': 'Marriage News', 'titleAr': 'أخبار الزواج', 'desc': 'Stay informed with the latest announcements.', 'descAr': 'ابقَ على اطلاع بأحدث الإعلانات.'},
                {'title': 'Emirates Discovery', 'titleAr': 'اكتشاف الإمارات', 'desc': 'Browse marriage support services, organizations.', 'descAr': 'تصفح خدمات دعم الزواج والمؤسسات.'},
                {'title': 'Community Support & Resources', 'titleAr': 'الدعم المجتمعي والموارد', 'desc': 'Access trusted charities, financial assistance programs.', 'descAr': 'الوصول إلى الجمعيات الخيرية الموثوقة وبرامج المساعدة المالية.'},
            ],

            'our_impact': 'Our Impact',
            'our_impact_ar': 'تأثيرنا',
            'our_impact_text': 'Measurable results that reflect our commitment to strengthening families.',
            'our_impact_text_ar': 'نتائج قابلة للقياس تعكس التزامنا بتعزيز الأسر.',
            'impact': [
                {'label': 'Total Emirates Support Initiatives', 'labelAr': 'إجمالي مبادرات الدعم في الإمارات', 'value': '240+ Support Initiatives', 'valueAr': 'أكثر من 240 مبادرة دعم'},
                {'label': 'Partner Organizations', 'labelAr': 'منظمات شريكة', 'value': '100+ Partner Organizations', 'valueAr': 'أكثر من 100 منظمة شريكة'},
                {'label': 'Consulting Program', 'labelAr': 'برنامج الاستشارات', 'value': '45+ Consultation Programs', 'valueAr': 'أكثر من 45 برنامج استشارات'},
                {'label': 'Community Members', 'labelAr': 'أعضاء المجتمع', 'value': '50,000+ Members Served', 'valueAr': 'أكثر من 50,000 عضو تم خدمتهم'},
            ],

            'why_choose': 'Why Choose Alia',
            'why_choose_ar': 'لماذا تختار عالية',
            'why_choose_text': 'Built with care, backed by trust, designed for every family.',
            'why_choose_text_ar': 'صُمّمت بعناية، مدعومة بالثقة، مصممة لكل أسرة.',
            'why_values': ['Trusted Information', 'Verified Organizations', 'Guided Experience', 'Easy Navigation'],

            'core_values': 'Our Core Values',
            'core_values_ar': 'قيمنا الجوهرية',
            'core_values_text': 'The principles that guide everything we do.',
            'core_values_text_ar': 'المبادئ التي توجه كل ما نفعله.',
            'core_value_list': ['Trust', 'Convenience', 'Accessibility', 'Innovation', 'Community'],

            'published': True,
        }

        obj, created = AboutContent.objects.update_or_create(
            pk=AboutContent.objects.first().pk if AboutContent.objects.exists() else None,
            defaults=data,
        )

        action = 'Created' if created else 'Updated'
        self.stdout.write(self.style.SUCCESS(f'{action} AboutContent (pk={obj.pk}) with {len(data)} fields.'))
