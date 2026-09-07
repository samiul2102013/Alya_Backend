"""Repair rows left with an empty slug by the old two-step create.

The old EmirateAdminSerializer.create() (and the other admin serializers)
inserted the row with slug='' and set the slug in a second query. If a
request died in between (deploy restart, crash, timeouts), the empty-slug
row stayed behind and its unique constraint made every subsequent create
fail with a 500. Backfill empty slugs so creates work again.
"""
from django.db import migrations
from django.utils.text import slugify


def backfill_empty_slugs(apps, schema_editor):
    Emirate = apps.get_model('content', 'Emirate')
    NewsArticle = apps.get_model('content', 'NewsArticle')
    Short = apps.get_model('content', 'Short')
    Initiative = apps.get_model('content', 'Initiative')
    Consultation = apps.get_model('content', 'Consultation')
    MediaItem = apps.get_model('content', 'MediaItem')

    def fix(model, name_field, fallback):
        taken = set(model.objects.exclude(slug='').values_list('slug', flat=True))
        for row in model.objects.filter(slug='').order_by('pk'):
            base = slugify(getattr(row, name_field) or '') or fallback
            slug, counter = base, 1
            while slug in taken:
                slug = f'{base}-{counter}'
                counter += 1
            row.slug = slug
            row.save(update_fields=['slug'])
            taken.add(slug)

    fix(Emirate, 'emirates_name', 'emirate')
    fix(NewsArticle, 'article_title', 'news')
    fix(Short, 'video_title', 'short')
    fix(Initiative, 'title', 'initiative')
    fix(Consultation, 'session_title', 'consultation')
    fix(MediaItem, 'filename', 'media')


def unbackfill(apps, schema_editor):
    # Data repair; nothing to reverse.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0011_pagepresentation_news_contributors_and_more'),
    ]

    operations = [
        migrations.RunPython(backfill_empty_slugs, unbackfill),
    ]
