from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='initiative',
            name='is_featured',
            field=models.BooleanField(
                default=False,
                help_text='If checked, this initiative is shown on the user panel hero (single featured).',
                verbose_name='Featured Initiative',
            ),
        ),
    ]
