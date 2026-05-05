import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'platforma.settings')
django.setup()

from django.contrib.auth.models import User
from listings.models import Category

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Admin izveidots: lietotajvards=admin, parole=admin123')

cats = [
    ('Auto', 'auto', 'car-front'),
    ('Nekustamais īpašums', 'nekustamais-ipasums', 'house'),
    ('Tehnika', 'tehnika', 'laptop'),
    ('Sadzīves preces', 'sadzives-preces', 'basket'),
    ('Apģērbs', 'apgerbs', 'bag'),
    ('Sports', 'sports', 'bicycle'),
    ('Dārzniecība', 'darzniecia', 'flower1'),
    ('Bērniem', 'berniem', 'emoji-smile'),
    ('Dzīvnieki', 'dzivnieki', 'heart'),
    ('Darbs', 'darbs', 'briefcase'),
    ('Pakalpojumi', 'pakalpojumi', 'tools'),
    ('Kolekcionēšana', 'kolekcionesana', 'trophy'),
]

for name, slug, icon in cats:
    obj, created = Category.objects.get_or_create(slug=slug, defaults={'name': name, 'icon': icon})
    print(f'{"Izveidota" if created else "Jau eksistē"}: {name}')

print('\nVisi dati pievienoti!')
