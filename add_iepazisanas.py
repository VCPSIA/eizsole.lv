import paramiko

HOST = '91.228.7.68'
USER = 'root'
PASS = 'F003xbFSplJyr44Z2B'

cmd = """
cd /var/www/eizsole && venv/bin/python manage.py shell << 'EOF'
from listings.models import Category
from django.utils.text import slugify
import re

def make_slug(name):
    slug = name.lower()
    slug = re.sub(r'[āä]', 'a', slug)
    slug = re.sub(r'[čc]', 'c', slug)
    slug = slug.replace('č', 'c').replace('ā', 'a').replace('ē', 'e').replace('ģ', 'g')
    slug = slug.replace('ī', 'i').replace('ķ', 'k').replace('ļ', 'l').replace('ņ', 'n')
    slug = slug.replace('š', 's').replace('ū', 'u').replace('ž', 'z')
    slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
    return slug

# Galvenā kategorija
parent, created = Category.objects.get_or_create(
    slug='iepazisanas',
    defaults={'name': 'Iepazīšanās', 'icon': 'ti ti-heart', 'order': 99}
)
if created:
    print(f'Izveidota: {parent.name}')
else:
    print(f'Jau eksistē: {parent.name}')

# Apakškategorijas
subcats = [
    ('Iepazīsies vīrietis ar sievieti', 'iepazisies-vietis-ar-sievieti'),
    ('Iepazīsies sieviete ar vīrieti', 'iepazisies-sieviete-ar-virieti'),
    ('Iepazīsies sieviete ar sievieti', 'iepazisies-sieviete-ar-sievieti'),
    ('Iepazīsies vīrietis ar vīrieti', 'iepazisies-vietis-ar-virieti'),
]

for name, slug in subcats:
    obj, created = Category.objects.get_or_create(
        slug=slug,
        defaults={'name': name, 'parent': parent, 'order': 0}
    )
    if created:
        print(f'  + {name}')
    else:
        print(f'  ~ jau eksistē: {name}')

print('Pabeigts!')
EOF
"""

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS)

_, stdout, stderr = ssh.exec_command(cmd)
out = stdout.read().decode()
err = stderr.read().decode()
print(out)
if err:
    print('KĻŪDA:', err)

ssh.close()
