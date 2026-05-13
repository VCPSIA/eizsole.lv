import paramiko

HOST = '91.228.7.68'
USER = 'root'
PASS = 'F003xbFSplJyr44Z2B'

cmd = """cd /var/www/eizsole && venv/bin/python manage.py shell << 'EOF'
from listings.models import Category
cats = Category.objects.filter(name__icontains='cits sports')
for c in cats:
    c.name = 'Cits'
    c.save()
    print(f'Pardēvets: slug={c.slug}')
if not cats:
    print('Nav atrasts')
EOF"""

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS)
_, stdout, _ = ssh.exec_command(cmd)
print(stdout.read().decode())
ssh.close()
