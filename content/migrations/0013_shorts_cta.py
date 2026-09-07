from django.db import migrations, models


def add_columns_if_not_exists(apps, schema_editor):
    table = 'content_pagepresentation'
    columns = [
        ('shorts_cta', 'jsonb', "DEFAULT '{}'::jsonb"),
    ]
    with schema_editor.connection.cursor() as cursor:
        if schema_editor.connection.vendor == 'postgresql':
            for col, col_type, default in columns:
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN IF NOT EXISTS {col} {col_type} {default};")
        else:
            existing = [row[1] for row in cursor.execute(f"PRAGMA table_info({table});").fetchall()]
            for col, _, _ in columns:
                if col not in existing:
                    cursor.execute(f"ALTER TABLE {table} ADD COLUMN {col} json DEFAULT '{{}}';")


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0012_backfill_empty_slugs'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(
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
            ],
            database_operations=[
                migrations.RunPython(add_columns_if_not_exists, noop_reverse),
            ],
        ),
    ]
