from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0033_add_offer_deal_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='SidebarBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot', models.PositiveSmallIntegerField(choices=[(1, '1. slots (augšā)'), (2, '2. slots (vidū)'), (3, '3. slots (apakšā)')], unique=True, verbose_name='Pozīcija')),
                ('title', models.CharField(blank=True, max_length=100, verbose_name='Nosaukums (tikai admin)')),
                ('image', models.ImageField(upload_to='sidebar_banners/', verbose_name='Attēls')),
                ('link_url', models.URLField(blank=True, verbose_name='Saite (pēc klikšķa)')),
                ('is_active', models.BooleanField(default=True, verbose_name='Aktīvs')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Sānjoslas baneris',
                'verbose_name_plural': 'Sānjoslas baneri',
                'ordering': ['slot'],
            },
        ),
    ]
