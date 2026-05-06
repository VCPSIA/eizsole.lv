from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0023_banner_sitesettings_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='text',
            field=models.CharField(blank=True, max_length=200, verbose_name='Teksts (rakstāmmašīna)'),
        ),
    ]
