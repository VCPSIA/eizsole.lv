import paramiko

HOST = '91.228.7.68'
USER = 'root'
PASS = 'F003xbFSplJyr44Z2B'

cmd = """cd /var/www/eizsole && venv/bin/python manage.py shell << 'EOF'
from listings.models import Category
try:
    cat = Category.objects.get(slug='sports')
    cat.name = 'Sports un hobijs'
    cat.save()
    print(f'Pārdēvēts: {cat.name} (slug: {cat.slug})')
except Category.DoesNotExist:
    # Meklē pēc nosaukuma
    cats = Category.objects.filter(name__icontains='sport')
    for c in cats:
        print(f'Atrasts: {c.name} slug={c.slug} parent={c.parent}')
EOF"""

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS)
_, stdout, _ = ssh.exec_command(cmd)
print(stdout.read().decode())
ssh.close()
