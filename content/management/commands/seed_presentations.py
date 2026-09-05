"""
Management command: seed_presentations

Updates (or creates) the PagePresentation records for:
- 'shorts'
- 'news'
- 'initiatives'
- 'consultation'
- 'emirates'

Populates topics, contributors, FAQs, and section visibility options.
Safe to run on an existing database — uses update_or_create / get_or_create.
Pass --force to overwrite existing topics, contributors, and FAQs.

Usage:
    python manage.py seed_presentations [--force]
"""

from django.core.management.base import BaseCommand
from content.models import PagePresentation


SHORTS_DATA = {
    'key': 'shorts',
    'title': 'Expert Marriage & Family Advice, in Short Videos',
    'title_ar': 'نصائح الخبراء في الزواج والأسرة، في فيديوهات قصيرة',
    'description': (
        'Concise, practical guidance from certified experts across the UAE. '
        'Watch, learn, and grow together - one short video at a time.'
    ),
    'description_ar': (
        'إرشادات موجزة وعملية من خبراء معتمدين في جميع أنحاء الإمارات. '
        'شاهد وتعلم وانمو معًا - فيديو قصير في كل مرة.'
    ),
    'badge': 'Quick, Practical Guidance',
    'hero_image': (
        'https://images.unsplash.com/photo-1529156069898-49953e39b3ac?q=80&w=900&auto=format&fit=crop'
    ),
    'shorts_topics': [
        {'title': 'Marriage Preparation', 'videos': '24 Videos'},
        {'title': 'Relationship Advice', 'videos': '25 Videos'},
        {'title': 'Financial Planning', 'videos': '18 Videos'},
        {'title': 'Family Well-being', 'videos': '32 Videos'},
        {'title': 'Counseling', 'videos': '15 Videos'},
        {'title': 'Parenting', 'videos': '28 Videos'},
    ],
    'shorts_contributors': [
        'Government Programs',
        'Family Court Experts',
        'Certified Counselors',
        'NGO Partners',
    ],
    'shorts_faqs': [
        {
            'question': 'Are the videos free to watch?',
            'questionAr': 'هل مشاهدة مقاطع الفيديو مجانية؟',
            'answer': 'Yes — all our educational shorts and full-length videos are completely free to access.',
            'answerAr': 'نعم — جميع مقاطع الفيديو التعليمية القصيرة والكاملة متاحة مجانًا.',
        },
        {
            'question': 'Can I share these videos with others?',
            'questionAr': 'هل يمكنني مشاركة هذه الفيديوهات مع الآخرين؟',
            'answer': 'Absolutely. You can share any video directly from the platform with family or friends.',
            'answerAr': 'بالتأكيد. يمكنك مشاركة أي فيديو مباشرةً من المنصة مع أفراد الأسرة والأصدقاء.',
        },
        {
            'question': 'How often are new videos added?',
            'questionAr': 'كم مرة تُضاف مقاطع فيديو جديدة؟',
            'answer': 'We add new content weekly. Our library is continuously updated by trusted contributors.',
            'answerAr': 'نضيف محتوى جديدًا أسبوعيًا. يتم تحديث مكتبتنا باستمرار من قِبل مساهمين موثوقين.',
        },
        {
            'question': 'Are subtitles or translations available?',
            'questionAr': 'هل تتوفر ترجمات أو ترجمات نصية؟',
            'answer': 'Yes — most videos include Arabic and English subtitles.',
            'answerAr': 'نعم — تتضمن معظم مقاطع الفيديو ترجمات نصية باللغتين العربية والإنجليزية.',
        },
    ],
    'shorts_section_visibility': {
        'hero': True,
        'topics': True,
        'contributors': True,
        'faqs': True,
    },
    'published': True,
}


NEWS_DATA = {
    'key': 'news',
    'title': 'Latest News & Community Updates',
    'title_ar': 'آخر الأخبار ومستجدات المجتمع',
    'description': (
        'Stay informed with the latest updates, programs, and announcements across the UAE. '
        'Empowering families and building stronger communities.'
    ),
    'description_ar': (
        'ابق على اطلاع بآخر التحديثات والبرامج والإعلانات في جميع أنحاء دولة الإمارات. '
        'تمكين الأسر وبناء مجتمعات أكثر ترابطًا.'
    ),
    'badge': 'Stay Informed',
    'hero_image': (
        'https://images.unsplash.com/photo-1504711434969-e33886168f5c?q=80&w=900&auto=format&fit=crop'
    ),
    'news_topics': [
        {'title': 'Family Well-being', 'videos': '15 Updates'},
        {'title': 'Community Programs', 'videos': '22 Updates'},
        {'title': 'Legal & Marital Rights', 'videos': '18 Updates'},
        {'title': 'Financial Support Grants', 'videos': '10 Updates'},
        {'title': 'Workshops & Events', 'videos': '14 Updates'},
        {'title': 'Youth & Marriage', 'videos': '20 Updates'},
    ],
    'news_contributors': [
        'Ministry of Community Development',
        'Family Development Foundation',
        'Judicial Department Advisors',
        'UAE Marriage Support Alliance',
    ],
    'news_faqs': [
        {
            'question': 'How often are news articles published?',
            'questionAr': 'كم مرة يتم نشر المقالات الإخبارية؟',
            'answer': 'We publish official news, announcements, and program launches on a weekly basis.',
            'answerAr': 'نقوم بنشر الأخبار الرسمية والإعلانات وإطلاق البرامج على أساس أسبوعي.',
        },
        {
            'question': 'Can community members submit news or story tips?',
            'questionAr': 'هل يمكن لأفراد المجتمع تقديم أخبار أو مقترحات؟',
            'answer': 'Yes, you can contact our editorial team via the Contact Us page to share relevant community initiatives.',
            'answerAr': 'نعم، يمكنك التواصل مع فريق التحرير عبر صفحة اتصل بنا لمشاركة المبادرات المجتمعية ذات الصلة.',
        },
        {
            'question': 'Are the announced initiatives official government programs?',
            'questionAr': 'هل المبادرات المعلنة هي برامج حكومية رسمية؟',
            'answer': 'All initiatives and programs featured in our news section are verified government or licensed NGO services.',
            'answerAr': 'جميع المبادرات والبرامج المعروضة في قسم الأخبار هي خدمات حكومية موثقة أو برامج لجمعيات نفع عام مرخصة.',
        },
    ],
    'news_section_visibility': {
        'hero': True,
        'topics': True,
        'contributors': True,
        'faqs': True,
    },
    'published': True,
}


INITIATIVES_DATA = {
    'key': 'initiatives',
    'title': 'National Initiatives & Family Programs',
    'title_ar': 'المبادرات الوطنية وبرامج الأسرة',
    'description': (
        'Explore nationwide projects and community programs designed to empower UAE families, '
        'support youth marriage, and foster household stability.'
    ),
    'description_ar': (
        'استكشف المشاريع الوطنية والبرامج المجتمعية المصممة لتمكين الأسر الإماراتية، '
        'ودعم زواج الشباب، وتعزيز الاستقرار الأسري.'
    ),
    'badge': 'Empowering UAE Families',
    'hero_image': (
        'https://images.unsplash.com/photo-1517048676732-d65bc937f952?q=80&w=900&auto=format&fit=crop'
    ),
    'initiatives_topics': [
        {'title': 'Marriage Grants & Funds', 'videos': '12 Programs'},
        {'title': 'Pre-Marital Preparation', 'videos': '16 Programs'},
        {'title': 'Housing & Settlement Support', 'videos': '8 Programs'},
        {'title': 'Parenting & Family Care', 'videos': '14 Programs'},
        {'title': 'Financial Literacy', 'videos': '10 Programs'},
        {'title': 'Youth Engagement & Guidance', 'videos': '11 Programs'},
    ],
    'initiatives_contributors': [
        'Marriage Fund (MOCD)',
        'Abu Dhabi Early Childhood Authority',
        'Dubai Community Development Authority',
        'Sharjah Family Development Center',
    ],
    'initiatives_faqs': [
        {
            'question': 'Who is eligible to apply for UAE marriage initiatives?',
            'questionAr': 'من المؤهل للتقديم على مبادرات الزواج في الإمارات؟',
            'answer': 'Eligibility varies by program. Most government marriage grants are available to UAE national couples meeting specific criteria.',
            'answerAr': 'تختلف معايير الأهلية حسب البرنامج. تتوفر معظم منح الزواج الحكومية للمواطنين الإماراتيين المستوفين للشروط المحددة.',
        },
        {
            'question': 'How do I apply for an initiative?',
            'questionAr': 'كيف يمكنني التقديم على إحدى المبادرات؟',
            'answer': 'Click on any initiative card to view details, required documents, and the direct link to the official application portal.',
            'answerAr': 'اضغط على بطاقة أي مبادرة لعرض التفاصيل والمستندات المطلوبة والرابط المباشر لبوابة التقديم الرسمية.',
        },
        {
            'question': 'Are there pre-marital workshops required?',
            'questionAr': 'هل يُشترط حضور ورش عمل تأهيلية قبل الزواج؟',
            'answer': 'Yes, several initiatives include or require pre-marital preparation courses to help couples build strong foundations.',
            'answerAr': 'نعم، تتضمن العديد من المبادرات أو تشترط دورات تأهيلية قبل الزواج لمساعدة الأزواج على بناء أسس أسرية متينة.',
        },
    ],
    'initiatives_section_visibility': {
        'hero': True,
        'topics': True,
        'contributors': True,
        'faqs': True,
    },
    'published': True,
}


CONSULTATION_DATA = {
    'key': 'consultation',
    'title': 'Confidential Family & Marriage Consultations',
    'title_ar': 'استشارات أسرية وزوجية بسرية تامة',
    'description': (
        'Book confidential sessions with certified marital, psychological, and legal experts across the UAE. '
        'Guiding you toward lasting family harmony and understanding.'
    ),
    'description_ar': (
        'احجز جلسات سرية مع مستشارين معتمدين في شؤون الزواج والنفسية والقانونية في جميع أنحاء الإمارات. '
        'نرشدكم نحو التوافق والاستقرار الأسري المستدام.'
    ),
    'badge': 'Confidential & Certified',
    'hero_image': (
        'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=900&auto=format&fit=crop'
    ),
    'consultation_topics': [
        {'title': 'Pre-Marital Compatibility', 'titleAr': 'التوافق قبل الزواج', 'videos': '25 Experts'},
        {'title': 'Marital Harmony & Communication', 'titleAr': 'التوافق والتواصل الزوجي', 'videos': '30 Experts'},
        {'title': 'Financial Planning & Budgeting', 'titleAr': 'التخطيط والميزانية المالية', 'videos': '16 Experts'},
        {'title': 'Parenting & Child Guidance', 'titleAr': 'تربية وتوجيه الأبناء', 'videos': '20 Experts'},
        {'title': 'Family Dispute Resolution', 'titleAr': 'حل الخلافات والنزاعات الأسرية', 'videos': '22 Experts'},
        {'title': 'Mental Health & Well-being', 'titleAr': 'الصحة النفسية والرفاه الأسري', 'videos': '18 Experts'},
    ],
    'consultation_contributors': [
        'Certified Family Counselors Association',
        'Judicial Mediation Advisors',
        'Child & Youth Psychology Experts',
        'National Mental Health Coalition',
    ],
    'consultation_faqs': [
        {
            'question': 'Are consultation sessions confidential?',
            'questionAr': 'هل جلسات الاستشارة سرية؟',
            'answer': 'Yes, all consultations adhere to strict confidentiality protocols governed by UAE privacy laws.',
            'answerAr': 'نعم، تلتزم جميع الاستشارات ببروتوكولات سرية تامة ومحمية بموجب قوانين الخصوصية في دولة الإمارات.',
        },
        {
            'question': 'Can I book a remote / virtual session?',
            'questionAr': 'هل يمكنني حجز جلسة استشارة عن بُعد؟',
            'answer': 'Yes, consultations are offered both in-person at approved family centers and online via secure video calls.',
            'answerAr': 'نعم، تتوفر الاستشارات حضوريًا في المراكز المعتمدة وكذلك عبر مكالمات فيديو آمنة عن بُعد.',
        },
        {
            'question': 'Is there a cost for government-supported consultations?',
            'questionAr': 'هل توجد رسوم على الاستشارات المدعومة حكوميًا؟',
            'answer': 'Most government and community-sponsored family counseling sessions are provided free of charge to UAE citizens and residents.',
            'answerAr': 'معظم جلسات الإرشاد الأسري المدعومة حكوميًا ومجتمعيًا تُقدم مجانًا للمواطنين والمقيمين في دولة الإمارات.',
        },
    ],
    'consultation_section_visibility': {
        'hero': True,
        'topics': True,
        'contributors': True,
        'faqs': True,
    },
    'published': True,
}


EMIRATES_DATA = {
    'key': 'emirates',
    'title': 'Support Services Across All 7 Emirates',
    'title_ar': 'خدمات الدعم الأسري في جميع الإمارات السبع',
    'description': (
        'Find localized family development centers, marriage clinics, and official resources '
        'available right in your home emirate.'
    ),
    'description_ar': (
        'ابحث عن مراكز التنمية الأسرية المحلية وعيادات الزواج والموارد الرسمية المتاحة مباشرة في إمارتك.'
    ),
    'badge': 'Across the UAE',
    'hero_image': (
        'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=900&auto=format&fit=crop'
    ),
    'emirates_topics': [
        {'title': 'Abu Dhabi', 'titleAr': 'أبوظبي', 'videos': 'All Centers & Programs'},
        {'title': 'Dubai', 'titleAr': 'دبي', 'videos': 'All Centers & Programs'},
        {'title': 'Sharjah', 'titleAr': 'الشارقة', 'videos': 'All Centers & Programs'},
        {'title': 'Ajman', 'titleAr': 'عجمان', 'videos': 'All Centers & Programs'},
        {'title': 'Umm Al Quwain', 'titleAr': 'أم القيوين', 'videos': 'All Centers & Programs'},
        {'title': 'Ras Al Khaimah', 'titleAr': 'رأس الخيمة', 'videos': 'All Centers & Programs'},
        {'title': 'Fujairah', 'titleAr': 'الفجيرة', 'videos': 'All Centers & Programs'},
    ],
    'emirates_contributors': [
        'Abu Dhabi Family Development Foundation',
        'Dubai Community Development Authority',
        'Sharjah Department of Social Services',
        'Ajman Community Development Center',
    ],
    'emirates_faqs': [
        {
            'question': 'Can I access services in an emirate different from my residence?',
            'questionAr': 'هل يمكنني الاستفادة من خدمات إمارة أخرى غير إمارة إقامتي؟',
            'answer': 'Federal services and virtual consultations are accessible across all emirates. Local emirate programs may require emirate residency.',
            'answerAr': 'الخدمات الاتحادية والاستشارات الافتراضية متاحة لجميع الإمارات، بينما قد تتطلب بعض البرامج المحلية إثبات الإقامة في الإمارة المعنية.',
        },
        {
            'question': 'How do I locate the nearest family center in my emirate?',
            'questionAr': 'كيف أجد أقرب مركز تنمية أسرية في إمارتي؟',
            'answer': 'Select your emirate from the list above to see all mapped centers, addresses, and direct contact numbers.',
            'answerAr': 'اختر إمارتك من القائمة أعلاه للاطلاع على المراكز المحددة وعناوينها وأرقام التواصل المباشرة.',
        },
    ],
    'emirates_section_visibility': {
        'hero': True,
        'topics': True,
        'contributors': True,
        'faqs': True,
    },
    'published': True,
}


PRESENTATIONS = [
    SHORTS_DATA,
    NEWS_DATA,
    INITIATIVES_DATA,
    CONSULTATION_DATA,
    EMIRATES_DATA,
]


class Command(BaseCommand):
    help = (
        'Seed (or refresh) PagePresentation entries for shorts, news, '
        'initiatives, consultation, and emirates. Safe to run on an existing database.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Overwrite topics/contributors/FAQs even if they are already populated.',
        )

    def handle(self, *args, **options):
        force = options.get('force', False)
        self.stdout.write(self.style.NOTICE('Seeding PagePresentation entries...'))

        for p_data in PRESENTATIONS:
            key = p_data['key']
            presentation, created = PagePresentation.objects.get_or_create(
                key=key,
                defaults=p_data,
            )

            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'  [+] Created {key} PagePresentation.'
                ))
            else:
                updated_fields = []
                # Core fields update if empty or forced
                for field in [
                    'title', 'title_ar', 'description', 'description_ar',
                    'badge', 'hero_image'
                ]:
                    if force or not getattr(presentation, field):
                        setattr(presentation, field, p_data[field])
                        updated_fields.append(field)

                # Topics, Contributors, FAQs, Section Visibility
                prefix = key
                extra_fields = [
                    f'{prefix}_topics',
                    f'{prefix}_contributors',
                    f'{prefix}_faqs',
                    f'{prefix}_section_visibility',
                ]

                for field in extra_fields:
                    if hasattr(presentation, field) and field in p_data:
                        current_val = getattr(presentation, field)
                        if force or not current_val:
                            setattr(presentation, field, p_data[field])
                            updated_fields.append(field)

                if updated_fields:
                    presentation.save(update_fields=list(set(updated_fields)))
                    self.stdout.write(self.style.SUCCESS(
                        f'  [*] Updated {key} PagePresentation (fields: {", ".join(set(updated_fields))}).'
                    ))
                else:
                    self.stdout.write(self.style.NOTICE(
                        f'  [-] {key} PagePresentation is already up to date.'
                    ))

        self.stdout.write(self.style.SUCCESS('Successfully seeded all PagePresentation entries.'))
