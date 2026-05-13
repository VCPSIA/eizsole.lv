from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0028_report_unique_reporter_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'Vīrietis'), ('female', 'Sieviete')], max_length=10),
        ),
        migrations.AddField(
            model_name='listing',
            name='seeking',
            field=models.CharField(blank=True, choices=[('male', 'Vīrietis'), ('female', 'Sieviete')], max_length=10),
        ),
    ]
