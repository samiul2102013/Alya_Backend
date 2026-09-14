# Generated manual — add Arabic mirrors + auto-translate support
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0016_footercontent_logo_and_headings'),
    ]

    operations = [
        # Short
        migrations.AddField(
            model_name='short',
            name='description_ar',
            field=models.TextField(blank=True, verbose_name='Description (Arabic)'),
        ),
        migrations.AddField(
            model_name='short',
            name='speaker_ar',
            field=models.CharField(blank=True, max_length=200, verbose_name='Speaker (Arabic)'),
        ),
        # NewsArticle
        migrations.AddField(
            model_name='newsarticle',
            name='content_ar',
            field=models.TextField(blank=True, verbose_name='Content (Arabic)'),
        ),
        migrations.AddField(
            model_name='newsarticle',
            name='author_ar',
            field=models.CharField(blank=True, max_length=200, verbose_name='Author (Arabic)'),
        ),
        # Initiative
        migrations.AddField(
            model_name='initiative',
            name='description_ar',
            field=models.TextField(blank=True, verbose_name='Description (Arabic)'),
        ),
        migrations.AddField(
            model_name='initiative',
            name='purpose_ar',
            field=models.TextField(blank=True, verbose_name='Purpose (Arabic)'),
        ),
        migrations.AddField(
            model_name='initiative',
            name='objectives_ar',
            field=models.JSONField(blank=True, default=list, verbose_name='Objectives (Arabic)'),
        ),
        migrations.AddField(
            model_name='initiative',
            name='badge_ar',
            field=models.CharField(blank=True, max_length=100, verbose_name='Badge (Arabic)'),
        ),
        migrations.AddField(
            model_name='initiative',
            name='benefits_ar',
            field=models.JSONField(blank=True, default=list, verbose_name='Benefits (Arabic)'),
        ),
        # Consultation
        migrations.AddField(
            model_name='consultation',
            name='counselor_ar',
            field=models.CharField(blank=True, max_length=200, verbose_name='Counselor (Arabic)'),
        ),
        migrations.AddField(
            model_name='consultation',
            name='counselor_title_ar',
            field=models.CharField(blank=True, max_length=200, verbose_name='Counselor Title (Arabic)'),
        ),
        migrations.AddField(
            model_name='consultation',
            name='counselor_bio_ar',
            field=models.TextField(blank=True, verbose_name='Counselor Bio (Arabic)'),
        ),
        migrations.AddField(
            model_name='consultation',
            name='description_ar',
            field=models.TextField(blank=True, verbose_name='Description (Arabic)'),
        ),
        migrations.AddField(
            model_name='consultation',
            name='objectives_ar',
            field=models.JSONField(blank=True, default=list, verbose_name='Objectives (Arabic)'),
        ),
        migrations.AddField(
            model_name='consultation',
            name='what_you_will_learn_ar',
            field=models.JSONField(blank=True, default=list, verbose_name='What You Will Learn (Arabic)'),
        ),
        migrations.AddField(
            model_name='consultation',
            name='who_should_attend_ar',
            field=models.JSONField(blank=True, default=list, verbose_name='Who Should Attend (Arabic)'),
        ),
        migrations.AddField(
            model_name='consultation',
            name='booking_notice_ar',
            field=models.CharField(blank=True, max_length=500, verbose_name='Booking Notice (Arabic)'),
        ),
        # Emirate
        migrations.AddField(
            model_name='emirate',
            name='title_ar',
            field=models.CharField(blank=True, max_length=200, verbose_name='Title (Arabic)'),
        ),
        migrations.AddField(
            model_name='emirate',
            name='description_ar',
            field=models.TextField(blank=True, verbose_name='Description (Arabic)'),
        ),
        migrations.AddField(
            model_name='emirate',
            name='center_count_ar',
            field=models.CharField(blank=True, max_length=100, verbose_name='Center Count (Arabic)'),
        ),
        # Category
        migrations.AddField(
            model_name='category',
            name='name_ar',
            field=models.CharField(blank=True, max_length=100, verbose_name='Category (Arabic)'),
        ),
        migrations.AddField(
            model_name='category',
            name='description_ar',
            field=models.TextField(blank=True, verbose_name='Description (Arabic)'),
        ),
    ]
