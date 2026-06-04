#!/usr/bin/env python3
"""Runs on VPS — simulates admin creating an auction and captures error message."""
import django, os, re, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'platforma.settings'
django.setup()
from django.test import Client
from django.contrib.auth.models import User
from listings.models import Category
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
cat = Category.objects.get(pk=119)  # Monetas - kas lietotajs izvelejas
ends = (timezone.now() + timedelta(days=3)).strftime('%Y-%m-%dT%H:%M')

c = Client()
c.force_login(user)

# Test 1: tira izsole ar bildi
img = SimpleUploadedFile('test.png', png, content_type='image/png')
r = c.post('/publicet/', {
    'title': 'DEBUG Izsole',
    'description': 'Debug tests',
    'category': cat.pk,
    'is_auction': 'on',
    'starting_price': '5.00',
    'ends_at': ends,
    'contact_phone': '+37126000000',
    'contact_email': 'admin@eizsole.lv',
    'images': img,
}, HTTP_HOST='eizsole.lv')

print('Status:', r.status_code)
if r.status_code in (301, 302):
    print('SUCCESS -> redirect:', r.get('Location'))
else:
    content = r.content.decode('utf-8', errors='replace')
    msgs = re.findall(r'class="alert[^"]*"[^>]*>(.*?)</div>', content, re.DOTALL)
    for m in msgs:
        clean = re.sub(r'<[^>]+>', ' ', m).strip()
        if clean and len(clean) > 3:
            print('KLUDAS ZINOJUMS:', clean[:300])

# Test 2: bilde nav - vajag kludu "Ludzu pievienojiet bildi"
r2 = c.post('/publicet/', {
    'title': 'DEBUG bez bildes',
    'description': 'Debug tests',
    'category': cat.pk,
    'is_auction': 'on',
    'starting_price': '5.00',
    'ends_at': ends,
    'contact_phone': '+37126000000',
    'contact_email': 'admin@eizsole.lv',
}, HTTP_HOST='eizsole.lv')
print('\nBez bildes status:', r2.status_code)
content2 = r2.content.decode('utf-8', errors='replace')
msgs2 = re.findall(r'class="alert[^"]*"[^>]*>(.*?)</div>', content2, re.DOTALL)
for m in msgs2:
    clean = re.sub(r'<[^>]+>', ' ', m).strip()
    if clean and len(clean) > 3:
        print('MSG:', clean[:200])
