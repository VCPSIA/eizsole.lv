import django, os, traceback
os.environ['DJANGO_SETTINGS_MODULE'] = 'platforma.settings'
django.setup()
from django.test import Client
from django.contrib.auth.models import User
from listings.models import Listing, Category, SiteSettings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from datetime import timedelta

png = bytes([
    0x89,0x50,0x4E,0x47,0x0D,0x0A,0x1A,0x0A,0x00,0x00,0x00,0x0D,0x49,0x48,0x44,0x52,
    0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x01,0x08,0x02,0x00,0x00,0x00,0x90,0x77,0x53,
    0xDE,0x00,0x00,0x00,0x0C,0x49,0x44,0x41,0x54,0x08,0xD7,0x63,0xF8,0xFF,0xFF,0x3F,
    0x00,0x05,0xFE,0x02,0xFE,0xDC,0xCC,0x59,0xE7,0x00,0x00,0x00,0x00,0x49,0x45,0x4E,
    0x44,0xAE,0x42,0x60,0x82
])

user = User.objects.get(username='admin')
cat = Category.objects.filter(parent__isnull=False).first()
c = Client()
c.force_login(user)

# 1. Publicē parastu sludinājumu
img = SimpleUploadedFile('t.png', png, content_type='image/png')
r1 = c.post('/publicet/', {
    'title': 'DEBUG Delete Test',
    'description': 'Testa sludinājums dzēšanai',
    'category': cat.pk,
    'price': '10.00',
    'deal_type': 'sell',
    'contact_phone': '+37126000000',
    'contact_email': 'admin@eizsole.lv',
    'duration': '7',
    'images': img,
}, HTTP_HOST='eizsole.lv')

print(f'Publicēšana: {r1.status_code} → {r1.get("Location", "nav redirect")}')

if r1.status_code not in (301, 302):
    print('KĻŪDA: sludinājums netika izveidots')
    exit(1)

pk = int(r1.get('Location').split('/')[-2])
print(f'Listing pk={pk}')

# 2. Moderācijas delete
try:
    r2 = c.post(f'/moderacija/{pk}/', {
        'action': 'delete',
        'admin_note': '',
    }, HTTP_HOST='eizsole.lv')
    print(f'Moderācija delete: {r2.status_code}')
    if r2.status_code == 500:
        print('=== 500 KĻŪDA ===')
        print(r2.content.decode('utf-8', errors='replace')[:500])
except Exception as e:
    print(f'IZŅĒMUMS: {e}')
    traceback.print_exc()

# 3. Arī pārbauda parasto delete_listing
img2 = SimpleUploadedFile('t2.png', png, content_type='image/png')
r3 = c.post('/publicet/', {
    'title': 'DEBUG Delete Test 2',
    'description': 'Testa sludinājums dzēšanai 2',
    'category': cat.pk,
    'price': '10.00',
    'deal_type': 'sell',
    'contact_phone': '+37126000000',
    'contact_email': 'admin@eizsole.lv',
    'duration': '7',
    'images': img2,
}, HTTP_HOST='eizsole.lv')

if r3.status_code in (301, 302):
    pk2 = int(r3.get('Location').split('/')[-2])
    print(f'\nListing 2 pk={pk2}')
    try:
        r4 = c.post(f'/sludinajums/{pk2}/dzest/', HTTP_HOST='eizsole.lv')
        print(f'delete_listing: {r4.status_code} → {r4.get("Location", "")}')
    except Exception as e:
        print(f'IZŅĒMUMS delete_listing: {e}')
        traceback.print_exc()
