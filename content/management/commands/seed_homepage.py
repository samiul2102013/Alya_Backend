from django.core.management.base import BaseCommand
from content.models import HomepageContent


class Command(BaseCommand):
    help = 'Seed HomepageContent with default EN/AR content from translations.'

    def handle(self, *args, **options):
        self.stdout.write('Seeding HomepageContent defaults...')

        data = {
            # ── Hero Section ──
            'hero_eyebrow': 'Supporting stronger families across the UAE',
            'hero_eyebrow_ar': 'ندعم أسراً أقوى في جميع أنحاء الإمارات',
            'hero_title': 'Building Stronger Families Through Trusted Marriage Support',
            'hero_title_ar': 'بناء أسر أقوى من خلال دعم زواج موثوق',
            'hero_subtitle': 'Alia is the official platform dedicated to guiding, supporting, and enriching marriage through government programs, expert consultation, and community initiatives.',
            'hero_subtitle_ar': 'عالية هي المنصة الرسمية المكرسة لتوجيه ودعم وإثراء الزواج من خلال البرامج الحكومية والاستشارات المتخصصة والمبادرات المجتمعية.',
            'hero_search_placeholder': 'Search Initiatives, Organizations, or Services...',
            'hero_search_placeholder_ar': 'ابحث عن المبادرات أو المؤسسات أو الخدمات...',
            'hero_search_button': 'Search',
            'hero_search_button_ar': 'بحث',
            'hero_primary_cta_label': 'Explore Initiatives',
            'hero_primary_cta_label_ar': 'استكشف المبادرات',
            'hero_primary_cta_link': '/initiatives',
            'hero_secondary_cta_label': 'Find Support',
            'hero_secondary_cta_label_ar': 'ابحث عن الدعم',
            'hero_secondary_cta_link': '/consultation',
            'hero_image': '',
            'hero_image_alt': 'Emirati family enjoying time together',
            'hero_floating_cards': [
                {'label': 'Government', 'labelAr': 'حكومية', 'sublabel': 'Programs', 'sublabelAr': 'برامج'},
                {'label': 'Consultation', 'labelAr': 'خدمات', 'sublabel': 'Services', 'sublabelAr': 'استشارية'},
                {'label': 'Upcoming', 'labelAr': 'فعاليات', 'sublabel': 'Events', 'sublabelAr': 'قادمة'},
                {'label': 'Financial', 'labelAr': 'دعم', 'sublabel': 'Support', 'sublabelAr': 'مالي'},
            ],

            # ── Stats ──
            'stats': [
                {'value': '25,000+', 'title': 'Couples Supported', 'titleAr': 'أزواج مدعومون', 'subtitle': 'Government processed applications', 'subtitleAr': 'طلبات تمت معالجتها حكومياً'},
                {'value': '120+', 'title': 'Government Initiatives', 'titleAr': 'مبادرة حكومية', 'subtitle': 'Active marriage support funds', 'subtitleAr': 'صناديق دعم زواج نشطة'},
                {'value': '98%', 'title': 'Satisfaction Rate', 'titleAr': 'نسبة الرضا', 'subtitle': 'Post-consultation feedback', 'subtitleAr': 'تقييم ما بعد الاستشارة'},
                {'value': '2.4M+', 'title': 'Total Visitors', 'titleAr': 'إجمالي الزوار', 'subtitle': 'Platform visitors to date', 'subtitleAr': 'زوار المنصة حتى الآن'},
            ],

            # ── Shorts Section ──
            'shorts_title': 'Featured Marriage Guidance & Shorts',
            'shorts_title_ar': 'إرشادات الزواج المميزة والمقاطع القصيرة',
            'shorts_subtitle': 'Watch quick educational reels and legal advice from certified marital counselors.',
            'shorts_subtitle_ar': 'شاهد مقاطع توعوية قصيرة ونصائح قانونية من مستشاري الزواج المعتمدين.',
            'shorts_cta_label': 'Watch Reel',
            'shorts_cta_label_ar': 'شاهد المقطع',
            'shorts_empty_text': 'No videos available yet. Check back soon.',
            'shorts_empty_text_ar': 'لا توجد فيديوهات منشورة بعد، عد قريبًا.',

            # ── News Section ──
            'news_title': 'Latest Marriage News',
            'news_title_ar': 'آخر أخبار الزواج',
            'news_subtitle': 'Stay updated with official policy releases, wedding grant updates, and community events.',
            'news_subtitle_ar': 'ابقَ على اطلاع على الإعلانات الرسمية وتحديثات منح الزواج والفعاليات المجتمعية.',
            'news_cta_label': 'Read Full Article',
            'news_cta_label_ar': 'اقرأ المقال كاملاً',

            # ── Initiatives Section ──
            'initiatives_title': 'Upcoming National Initiatives',
            'initiatives_title_ar': 'المبادرات الوطنية القادمة',
            'initiatives_subtitle': 'Empowering Emirati youth with long-term marital stability and family support programs.',
            'initiatives_subtitle_ar': 'تمكين الشباب الإماراتي من الاستقرار الأسري طويل المدى وبرامج دعم الأسرة.',
            'initiatives_cta_label': 'Learn More & Register',
            'initiatives_cta_label_ar': 'اعرف المزيد وسجّل',

            # ── Consultations Section ──
            'consultations_title': 'Congratulations Sessions',
            'consultations_title_ar': 'جلسات تهنئة',
            'consultations_subtitle': 'Connect with certified expert and counselors to guide you through various stages of your merital journey.',
            'consultations_subtitle_ar': 'تواصل مع الخبراء والمستشارين المعتمدين لإرشادك في مختلف مراحل رحلتك الزوجية.',
            'consultations_cta_label': 'Book Now',
            'consultations_cta_label_ar': 'احجز الآن',
            'consultations_free_tab': 'Free Session',
            'consultations_free_tab_ar': 'جلسة مجانية',
            'consultations_paid_tab': 'Paid Session',
            'consultations_paid_tab_ar': 'جلسة مدفوعة',

            # ── Emirates Section ──
            'emirates_title': 'Explore Marriage Support by Emirate',
            'emirates_title_ar': 'استكشف دعم الزواج حسب الإمارة',
            'emirates_subtitle': 'Locate dedicated marriage support offices, council centers, and event venues in your emirate.',
            'emirates_subtitle_ar': 'حدد مكاتب دعم الزواج المخصصة ومراكز المجالس وأماكن الفعاليات في إمارتك.',
            'emirates_capital_label': 'Capital Region',
            'emirates_capital_label_ar': 'منطقة العاصمة',
            'emirates_headquarters_label': 'Main Headquarters',
            'emirates_headquarters_label_ar': 'المقر الرئيسي',
            'emirates_cta_label': 'Explore Centers',
            'emirates_cta_label_ar': 'استكشف المراكز',

            # ── CTA Section ──
            'cta_title': 'Start Your Journey Toward a Stronger Family',
            'cta_title_ar': 'ابدأ رحلتك نحو أسرة أقوى',
            'cta_subtitle': 'Join thousands of Emirati couples building lasting, happy futures with official government guidance, financial grants, and lifelong support.',
            'cta_subtitle_ar': 'انضم إلى آلاف الأزواج الإماراتيين الذين يبنون مستقبلاً سعيداً ودائماً مع الإرشاد الحكومي الرسمي والمنح المالية والدعم مدى الحياة.',
            'cta_primary_label': 'Explore Initiatives',
            'cta_primary_label_ar': 'استكشف المبادرات',
            'cta_primary_link': '/initiatives',
            'cta_secondary_label': 'Find Consultation',
            'cta_secondary_label_ar': 'ابحث عن استشارة',
            'cta_secondary_link': '/consultation',

            # ── Visibility ──
            'published': True,
        }

        obj, created = HomepageContent.objects.update_or_create(
            pk=HomepageContent.objects.first().pk if HomepageContent.objects.exists() else None,
            defaults=data,
        )

        action = 'Created' if created else 'Updated'
        self.stdout.write(self.style.SUCCESS(f'{action} HomepageContent (pk={obj.pk}) with {len(data)} fields.'))
