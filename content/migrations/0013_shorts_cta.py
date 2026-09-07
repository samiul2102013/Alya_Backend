from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0012_backfill_empty_slugs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagepresentation',
            name='shorts_cta',
            field=models.JSONField(
                blank=True,
                default=dict,
                help_text=(
                    'Text for the "Explore More Marriage Support" banner at the bottom of the '
                    'Shorts page. Keys: title, titleAr, text, textAr, browseLabel, browseLabelAr, '
                    'exploreLabel, exploreLabelAr.'
                ),
                verbose_name='Shorts CTA Banner',
            ),
        ),
    ]
