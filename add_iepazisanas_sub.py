import paramiko

HOST = '91.228.7.68'
USER = 'root'
PASS = 'F003xbFSplJyr44Z2B'

cmd = """
cd /var/www/eizsole && venv/bin/python manage.py shell << 'EOF'
from listings.models import Category

parents = [
    'iepazisies-vietis-ar-sievieti',
    'iepazisies-sieviete-ar-virieti',
    'iepazisies-sieviete-ar-sievieti',
    'iepazisies-vietis-ar-virieti',
]

subcats = [
    ('Izklaide',             'izklaide'),
    ('Nopietnas attiecības', 'nopietnas-attiecibas'),
    ('Ceļošana',             'celoshana'),
    ('Cits',                 'cits'),
]

for parent_slug in parents:
    try:
        parent = Category.objects.get(slug=parent_slug)
    except Category.DoesNotExist:
        print(f'Nav atrasts: {parent_slug}')
        continue
    for name, slug_suffix in subcats:
        slug = f'{parent_slug}-{slug_suffix}'
        obj, created = Category.objects.get_or_create(
            slug=slug,
            defaults={'name': name, 'parent': parent, 'order': 0}
        )
        if created:
            print(f'  + {parent.name} → {name}')
        else:
            print(f'  ~ jau eksistē: {slug}')

print('Pabeigts!')
EOF
"""

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS)

_, stdout, stderr = ssh.exec_command(cmd)
out = stdout.read().decode()
err = stderr.read().decode()
print(out.encode('utf-8', errors='replace').decode('utf-8'))
if err:
    print('KĻŪDA:', err[-500:].encode('utf-8', errors='replace').decode('utf-8'))

ssh.close()
