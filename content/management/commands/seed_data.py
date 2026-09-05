from django.core.management.base import BaseCommand

from accounts.models import AdminUser, PrivacyPolicy, Terms
from content.models import Category, Consultation, Emirate, Initiative, NewsArticle, PagePresentation, Short


class Command(BaseCommand):
    help = 'Seed demo data: admin user, emirates, categories, and sample content.'

    def handle(self, *args, **options):
        if not AdminUser.objects.filter(email='admin@maragesupport.ae').exists():
            AdminUser.objects.create_superuser(
                email='admin@maragesupport.ae',
                username='admin',
                name='Marage Admin',
                password='admin12345',
            )
            self.stdout.write(self.style.SUCCESS('Created superuser admin@maragesupport.ae / admin12345'))
        else:
            self.stdout.write('Admin user already exists.')

        if not PrivacyPolicy.objects.exists():
            PrivacyPolicy.objects.create(content='<p>Privacy policy pending.</p>')
        if not Terms.objects.exists():
            Terms.objects.create(content='<p>Terms pending.</p>')

        emirates = [
            ('abudhabi', 'Abu Dhabi', 'أبوظبي', 'Abu Dhabi - Marriage Support & Family Programs',
             'Abu Dhabi, the capital of the UAE, offers the widest range of government-backed marriage funds, family development programs, and expert pre-marital counseling across the emirate.',
             'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=900&auto=format&fit=crop'),
            ('dubai', 'Dubai', 'دبي', 'Dubai - Modern Family & Counseling Hub',
             'Dubai combines a modern global community with developed authorities and a wide network of private counseling centers devoted to family well-being.',
             'https://images.unsplash.com/photo-1518684079-3c830dcef090?q=80&w=900&auto=format&fit=crop'),
            ('sharjah', 'Sharjah', 'الشارقة', 'Sharjah - Heritage & Family Well-being',
             'Sharjah, the cultural capital, is home to heritage-focused family initiatives, educational programs, and social cohesion projects that strengthen marriage bonds.',
             'https://images.unsplash.com/photo-1584551246679-0daf3d275d0f?q=80&w=900&auto=format&fit=crop'),
            ('ajman', 'Ajman', 'عجمان', 'Ajman - Growing Community Support',
             'Ajman, a close-knit and fast-growing emirate, provides accessible marriage support programs, counseling services, and helpful community development initiatives.',
             'https://images.unsplash.com/photo-1465414829459-d228b58caf6e?q=80&w=900&auto=format&fit=crop'),
            ('rasalkhaimah', 'Ras Al Khaimah', 'رأس الخيمة', 'Ras Al Khaimah - Northern Family Programs',
             'Ras Al Khaimah offers strong community development programs, dedicated family guidance services, and reliable local marriage support within a scenic northern setting.',
             'https://images.unsplash.com/photo-1571896349842-33c89424de2d?q=80&w=900&auto=format&fit=crop'),
            ('fujairah', 'Fujairah', 'الفجيرة', 'Fujairah - Coastal Family Services',
             'Fujairah, a scenic coastal emirate, provides family support services, community resources, and personalized counseling programs that promote healthy, lasting relationships.',
             'https://images.unsplash.com/photo-1587474260584-136574528ed5?q=80&w=900&auto=format&fit=crop'),
            ('ummAlquwain', 'Umm Al-Quwain', 'أم القيوين', 'Umm Al Quwain - Personalized Family Guidance',
             'Umm Al Quwain, a peaceful emirate, offers personalized family guidance, emerging marriage support programs, and carefully tailored community resources for local families.',
             'https://images.unsplash.com/photo-1528702748617-c64d49f918af?q=80&w=900&auto=format&fit=crop'),
        ]
        for slug, name, name_ar, title, description, image in emirates:
            Emirate.objects.update_or_create(
                slug=slug,
                defaults={
                    'emirates_name': name,
                    'emirates_name_ar': name_ar,
                    'title': title,
                    'description': description,
                    'image': image,
                    'status': 'Published',
                },
            )
        self.stdout.write(self.style.SUCCESS('Emirates seeded.'))

        categories = [
            ('Marriage', 'Marriage-related content'),
            ('Family', 'Family-related content'),
            ('Education', 'Education content'),
            ('Finance', 'Financial support'),
            ('Health', 'Health and wellbeing'),
            ('Culture', 'Culture and heritage'),
            ('Service', 'Services and initiatives'),
        ]
        for name, desc in categories:
            if not Category.objects.filter(name=name).exists():
                Category.objects.create(name=name, description=desc)
        self.stdout.write(self.style.SUCCESS('Categories seeded.'))

        if not Short.objects.exists():
            Short.objects.create(
                slug='marriage-guidance', video_title='Marriage Guidance Basics',
                category='Education', organization='Marage', marital_stage='premarital',
                duration='4:30', status='Published',
                cover_image='http://127.0.0.1:8000/media/uploads/01c7c028fff94d219a158ba53c263939.png',
                video_url='http://127.0.0.1:8000/media/uploads/f759dc510080430caa5db252fcf097f8.mp4',
            )
        if not NewsArticle.objects.exists():
            NewsArticle.objects.create(
                slug='family-fund-announcement', article_title='New Family Fund Announcement',
                category='family', source='government', status='Published',
            )
        if not Initiative.objects.exists():
            Initiative.objects.create(
                slug='marriage-fund', title='Marriage Fund',
                category='Finance', emirates='abudhabi', badge='New',
                start_date='2025-01-01', end_date='2025-12-31', status='Published',
            )
        if not Consultation.objects.exists():
            Consultation.objects.create(
                slug='premarital-workshop', session_title='Premarital Workshop',
                category='Education', session_type='workshop', emirates='dubai',
                date='2026-01-15', start_time='10:00', end_time='12:00', duration='2 hours',
                is_free=True, status='Published',
            )

        presentations = [
            {
                'key': 'news',
                'title': 'Stay Informed with the Latest Marriage & Family News Across the UAE.',
                'title_ar': 'ابقَ على اطلاع بآخر أخبار الزواج والأسرة في دولة الإمارات.',
                'description': 'Explore curated news, updates, and announcements from trusted government agencies, family organizations, and community initiatives.',
                'description_ar': 'استكشف الأخبار والتنبيهات والتحديثات من الجهات الحكومية الموثوقة ومنظمات الأسرة ومبادرات المجتمع.',
                'badge': 'Latest Updates',
                'hero_image': 'https://images.unsplash.com/photo-1495020689067-958852a7765e?q=80&w=1200&auto=format&fit=crop',
            },
            {
                'key': 'shorts',
                'title': 'Expert Marriage & Family Advice, in Short Videos',
                'title_ar': 'نصائح الخبراء في الزواج والأسرة، في فيديوهات قصيرة',
                'description': 'Concise, practical guidance from certified experts across the UAE. Watch, learn, and grow together - one short video at a time.',
                'description_ar': 'إرشادات موجزة وعملية من خبراء معتمدين في جميع أنحاء الإمارات. شاهد وتعلم وانمو معًا - فيديو قصير في كل مرة.',
                'badge': 'Quick, Practical Guidance',
                'hero_image': 'https://images.unsplash.com/photo-1529156069898-49953e39b3ac?q=80&w=900&auto=format&fit=crop',
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
                        'answer': 'Yes — all our educational shorts and full-length videos are completely free to access. Simply browse the topic that interests you and start watching.',
                        'answerAr': 'نعم — جميع مقاطع الفيديو التعليمية القصيرة والكاملة متاحة مجانًا. ما عليك سوى تصفح الموضوع الذي يثير اهتمامك والبدء في المشاهدة.',
                    },
                    {
                        'question': 'Can I share these videos with others?',
                        'questionAr': 'هل يمكنني مشاركة هذه الفيديوهات مع الآخرين؟',
                        'answer': 'Absolutely. You can share any video directly from the platform with family, friends, or community groups to help spread awareness.',
                        'answerAr': 'بالتأكيد. يمكنك مشاركة أي فيديو مباشرةً من المنصة مع أفراد الأسرة والأصدقاء أو مجموعات المجتمع للمساعدة في نشر الوعي.',
                    },
                    {
                        'question': 'How often are new videos added?',
                        'questionAr': 'كم مرة تُضاف مقاطع فيديو جديدة؟',
                        'answer': 'We add new content weekly. Our library is continuously updated by trusted contributors and certified counselors to ensure fresh, relevant material.',
                        'answerAr': 'نضيف محتوى جديدًا أسبوعيًا. يتم تحديث مكتبتنا باستمرار من قِبل مساهمين موثوقين ومستشارين معتمدين لضمان تقديم مواد جديدة وذات صلة.',
                    },
                    {
                        'question': 'Are subtitles or translations available?',
                        'questionAr': 'هل تتوفر ترجمات أو ترجمات نصية؟',
                        'answer': 'Yes — most videos include Arabic and English subtitles. Additional language support is being rolled out gradually.',
                        'answerAr': 'نعم — تتضمن معظم مقاطع الفيديو ترجمات نصية باللغتين العربية والإنجليزية. ويجري طرح دعم لغات إضافية تدريجيًا.',
                    },
                ],
            },
            {
                'key': 'consultation',
                'title': 'Find the Right Marriage Consultation Session for a Stronger and Happier Future.',
                'title_ar': 'ابحث عن جلسة الاستشارة الزوجية المناسبة لمستقبل أقوى وأكثر سعادة.',
                'description': 'Explore free and paid consultation sessions offered by trusted government agencies, private organizations, and certified professionals across the UAE.',
                'description_ar': 'استكشف جلسات استشارية مجانية ومدفوعة تقدمها جهات حكومية ومنظمات خاصة ومختصون معتمدون في جميع أنحاء الإمارات.',
                'badge': 'Expert Guidance',
                'hero_image': 'https://images.unsplash.com/photo-1551836022-d5d88e9218df?q=80&w=900&auto=format&fit=crop',
            },
            {
                'key': 'initiatives',
                'title': 'Explore Marriage Support Initiatives Across the UAE',
                'title_ar': 'استكشف مبادرات دعم الزواج في دولة الإمارات',
                'description': 'Financial support, housing grants, education programs and more for eligible Emirati families.',
                'description_ar': 'دعم مالي ومنح إسكان وبرامج تعليمية والمزيد للأسر الإماراتية المؤهلة.',
                'badge': 'Featured Initiative',
                'hero_image': 'https://images.unsplash.com/photo-1523240795612-9a054b0db644?q=80&w=1200&auto=format&fit=crop',
            },
            {
                'key': 'emirates',
                'title': 'Discover marriage support services across the UAE Emirates',
                'title_ar': 'اكتشف خدمات دعم الزواج في إمارات دولة الإمارات',
                'description': 'Find consultation, financial help, counseling and community resources close to home in every emirate.',
                'description_ar': 'ابحث عن الاستشارة والدعم المالي والإرشاد والموارد المجتمعية بالقرب منك في كل إمارة.',
                'badge': 'Nationwide Coverage',
                'hero_image': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=1200&auto=format&fit=crop',
            },
        ]
        for p in presentations:
            PagePresentation.objects.update_or_create(key=p['key'], defaults=p)
        self.stdout.write(self.style.SUCCESS('Page presentations seeded.'))

        self.stdout.write(self.style.SUCCESS('Sample content seeded.'))