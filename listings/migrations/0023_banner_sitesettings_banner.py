from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0022_favorite'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='banner_enabled',
            field=models.BooleanField(default=False, verbose_name='Baneri ieslēgti'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='banner_fee',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=8, verbose_name='Banera maksa (€ ar PVN)'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='banner_rotation_seconds',
            field=models.PositiveIntegerField(default=5, verbose_name='Banera rotācijas laiks (sekundes)'),
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='banners/', verbose_name='Attēls')),
                ('link_url', models.URLField(blank=True, verbose_name='Saite (pēc klikšķa)')),
                ('is_active', models.BooleanField(default=True, verbose_name='Aktīvs')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('listing', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='banner', to='listings.listing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='banners', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Baneris',
                'verbose_name_plural': 'Baneri',
                'ordering': ['created_at'],
            },
        ),
    ]
