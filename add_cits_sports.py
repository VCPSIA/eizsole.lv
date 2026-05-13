import paramiko

HOST = '91.228.7.68'
USER = 'root'
PASS = 'F003xbFSplJyr44Z2B'

cmd = """cd /var/www/eizsole && venv/bin/python manage.py shell << 'EOF'
from listings.models import Category
parent = Category.objects.get(slug='sports')
obj, created = Category.objects.get_or_create(
    slug='sports-cits',
    defaults={'name': 'Cits', 'parent': parent, 'order': 99}
)
print('Izveidots' if created else 'Jau eksiste')
EOF"""

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS)
_, stdout, _ = ssh.exec_command(cmd)
print(stdout.read().decode())
ssh.close()
