import django, os, re
os.environ['DJANGO_SETTINGS_MODULE'] = 'platforma.settings'
django.setup()
from django.test import Client
from django.contrib.auth.models import User
from listings.models import Category
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from datetime import timedelta

with open('test_img.png', 'rb') as f:
    png = f.read()

cat = Category.objects.filter(parent__isnull=False, children__isnull=True).first()
user = User.objects.filter(is_active=True).first()
c = Client()
c.force_login(user)

def check(label, resp):
    loc = resp.get('Location', '')
    if resp.status_code in (301, 302):
        print(f'OK  {label}: {resp.status_code} -> {loc}')
    else:
        content = resp.content.decode('utf-8', errors='replace')
        msgs = re.findall(r'class="alert[^"]*"[^>]*>(.*?)</div>', content, re.DOTALL)
        errs = [re.sub(r'<[^>]+>', ' ', m).strip()[:120] for m in msgs if re.sub(r'<[^>]+>', '', m).strip()]
        print(f'ERR {label}: {resp.status_code} | {errs[:2]}')

# 1. Parasts sludinājums ar cenu
r = c.post('/publicet/', {
    'title': 'Parasts slud', 'description': 'Apraksts',
    'category': cat.pk, 'price': '50.00', 'deal_type': 'buy',
    'contact_phone': '+37126000000', 'contact_email': 'a@b.lv',
    'duration': '7', 'images': SimpleUploadedFile('t.png', png, content_type='image/png')
}, SERVER_NAME='127.0.0.1', HTTP_HOST='127.0.0.1:8000')
check('Parasts sludinājums (cena=50)', r)

# 2. Parasts BEZ cenas — kļūdai jābūt
r2 = c.post('/publicet/', {
    'title': 'Bez cenas', 'description': 'Apraksts',
    'category': cat.pk, 'price': '', 'deal_type': 'buy',
    'contact_phone': '+37126000000', 'contact_email': 'a@b.lv',
    'duration': '7', 'images': SimpleUploadedFile('t.png', png, content_type='image/png')
}, SERVER_NAME='127.0.0.1', HTTP_HOST='127.0.0.1:8000')
check('Parasts bez cenas (vajag kļūdu)', r2)

# 3. Izsole ar price=0 (lietotājs ievadīja cenu, tad atzīmēja izsoli)
ends = (timezone.now() + timedelta(days=3)).strftime('%Y-%m-%dT%H:%M')
r3 = c.post('/publicet/', {
    'title': 'Izsole price=0', 'description': 'Apraksts',
    'category': cat.pk, 'is_auction': 'on',
    'starting_price': '10.00', 'ends_at': ends,
    'price': '0', 'deal_type': 'buy',
    'contact_phone': '+37126000000', 'contact_email': 'a@b.lv',
    'images': SimpleUploadedFile('t.png', png, content_type='image/png')
}, SERVER_NAME='127.0.0.1', HTTP_HOST='127.0.0.1:8000')
check('Izsole (price=0, deal_type=buy)', r3)

# 4. Izsole tīra (bez price un deal_type)
r4 = c.post('/publicet/', {
    'title': 'Tīra izsole', 'description': 'Apraksts',
    'category': cat.pk, 'is_auction': 'on',
    'starting_price': '10.00', 'ends_at': ends,
    'contact_phone': '+37126000000', 'contact_email': 'a@b.lv',
    'images': SimpleUploadedFile('t.png', png, content_type='image/png')
}, SERVER_NAME='127.0.0.1', HTTP_HOST='127.0.0.1:8000')
check('Tīra izsole (nav price/deal_type)', r4)
