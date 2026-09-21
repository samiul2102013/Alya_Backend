from django.db import migrations


def align_hero_secondary_cta_with_news_label(apps, schema_editor):
    """Bug-18: the homepage hero button labelled "Latest news" was redirecting
    to /consultation (stale seeded link) instead of the news page.

    Repair rows where the secondary CTA label clearly refers to news but the
    link points elsewhere. Intentional pairs (e.g. "Find Support" -> /consultation)
    are left untouched.
    """
    HomepageContent = apps.get_model('content', 'HomepageContent')
    for page in HomepageContent.objects.all():
        label_en = (page.hero_secondary_cta_label or '').lower()
        label_ar = (page.hero_secondary_cta_label_ar or '')
        link = (page.hero_secondary_cta_link or '').strip()
        mentions_news = (
            'news' in label_en
            or 'news' in label_ar.lower()
            or 'أخبار' in label_ar
            or 'اخبار' in label_ar
        )
        if mentions_news and 'news' not in link.lower():
            page.hero_secondary_cta_link = '/news'
            page.save(update_fields=['hero_secondary_cta_link'])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0024_emirate_browse_initiatives_url'),
    ]

    operations = [
        migrations.RunPython(align_hero_secondary_cta_with_news_label, noop),
    ]
