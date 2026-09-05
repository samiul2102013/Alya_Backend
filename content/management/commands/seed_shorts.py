"""
Management command: seed_shorts

Updates (or creates) the 'shorts' PagePresentation with the default
topics, contributors, and FAQs that match the user-panel i18n defaults.

Safe to run on an existing database — it uses update_or_create so it will
not duplicate records. Existing values are overwritten only for the shorts
presentation.

Usage:
    python manage.py seed_shorts
"""

from django.core.management.base import BaseCommand

from content.models import PagePresentation


DEFAULT_TOPICS = [
    {'title': 'Marriage Preparation', 'videos': '24 Videos'},
    {'title': 'Relationship Advice',  'videos': '25 Videos'},
    {'title': 'Financial Planning',   'videos': '18 Videos'},
    {'title': 'Family Well-being',    'videos': '32 Videos'},
    {'title': 'Counseling',           'videos': '15 Videos'},
    {'title': 'Parenting',            'videos': '28 Videos'},
]

DEFAULT_CONTRIBUTORS = [
    'Government Programs',
    'Family Court Experts',
    'Certified Counselors',
    'NGO Partners',
]

DEFAULT_FAQS = [
    {
        'question':   'Are the videos free to watch?',
        'questionAr': 'هل مشاهدة مقاطع الفيديو مجانية؟',
        'answer':     (
            'Yes — all our educational shorts and full-length videos are completely free to '
            'access. Simply browse the topic that interests you and start watching.'
        ),
        'answerAr':   (
            'نعم — جميع مقاطع الفيديو التعليمية القصيرة والكاملة متاحة مجانًا. '
            'ما عليك سوى تصفح الموضوع الذي يثير اهتمامك والبدء في المشاهدة.'
        ),
    },
    {
        'question':   'Can I share these videos with others?',
        'questionAr': 'هل يمكنني مشاركة هذه الفيديوهات مع الآخرين؟',
        'answer':     (
            'Absolutely. You can share any video directly from the platform with family, '
            'friends, or community groups to help spread awareness.'
        ),
        'answerAr':   (
            'بالتأكيد. يمكنك مشاركة أي فيديو مباشرةً من المنصة مع أفراد الأسرة والأصدقاء '
            'أو مجموعات المجتمع للمساعدة في نشر الوعي.'
        ),
    },
    {
        'question':   'How often are new videos added?',
        'questionAr': 'كم مرة تُضاف مقاطع فيديو جديدة؟',
        'answer':     (
            'We add new content weekly. Our library is continuously updated by trusted '
            'contributors and certified counselors to ensure fresh, relevant material.'
        ),
        'answerAr':   (
            'نضيف محتوى جديدًا أسبوعيًا. يتم تحديث مكتبتنا باستمرار من قِبل مساهمين '
            'موثوقين ومستشارين معتمدين لضمان تقديم مواد جديدة وذات صلة.'
        ),
    },
    {
        'question':   'Are subtitles or translations available?',
        'questionAr': 'هل تتوفر ترجمات أو ترجمات نصية؟',
        'answer':     (
            'Yes — most videos include Arabic and English subtitles. Additional language '
            'support is being rolled out gradually.'
        ),
        'answerAr':   (
            'نعم — تتضمن معظم مقاطع الفيديو ترجمات نصية باللغتين العربية والإنجليزية. '
            'ويجري طرح دعم لغات إضافية تدريجيًا.'
        ),
    },
]


class Command(BaseCommand):
    help = (
        'Seed (or refresh) the Shorts PagePresentation with default topics, '
        'contributors, and FAQs. Safe to run on an existing database.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Overwrite topics/contributors/FAQs even if they are already populated.',
        )

    def handle(self, *args, **options):
        force = options['force']

        presentation, created = PagePresentation.objects.get_or_create(
            key='shorts',
            defaults={
                'title':       'Expert Marriage & Family Advice, in Short Videos',
                'title_ar':    'نصائح الخبراء في الزواج والأسرة، في فيديوهات قصيرة',
                'description': (
                    'Concise, practical guidance from certified experts across the UAE. '
                    'Watch, learn, and grow together - one short video at a time.'
                ),
                'description_ar': (
                    'إرشادات موجزة وعملية من خبراء معتمدين في جميع أنحاء الإمارات. '
                    'شاهد وتعلم وانمو معًا - فيديو قصير في كل مرة.'
                ),
                'badge':      'Quick, Practical Guidance',
                'hero_image': (
                    'https://images.unsplash.com/photo-1529156069898-49953e39b3ac'
                    '?q=80&w=900&auto=format&fit=crop'
                ),
                'shorts_topics':       DEFAULT_TOPICS,
                'shorts_contributors': DEFAULT_CONTRIBUTORS,
                'shorts_faqs':         DEFAULT_FAQS,
                'published':           True,
            },
        )

        if created:
            self.stdout.write(self.style.SUCCESS(
                'Created shorts PagePresentation with default topics, contributors, and FAQs.'
            ))
            return

        # Already exists — only overwrite extras if empty or --force passed
        updated_fields = []

        if force or not presentation.shorts_topics:
            presentation.shorts_topics = DEFAULT_TOPICS
            updated_fields.append('shorts_topics')

        if force or not presentation.shorts_contributors:
            presentation.shorts_contributors = DEFAULT_CONTRIBUTORS
            updated_fields.append('shorts_contributors')

        if force or not presentation.shorts_faqs:
            presentation.shorts_faqs = DEFAULT_FAQS
            updated_fields.append('shorts_faqs')

        if updated_fields:
            presentation.save(update_fields=updated_fields)
            self.stdout.write(self.style.SUCCESS(
                f'Updated shorts presentation: {", ".join(updated_fields)}'
            ))
        else:
            self.stdout.write(
                'Shorts presentation already has topics, contributors, and FAQs. '
                'Use --force to overwrite.'
            )
