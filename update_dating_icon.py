import paramiko

HOST = '91.228.7.68'
USER = 'root'
PASS = 'F003xbFSplJyr44Z2B'

cmd = """cd /var/www/eizsole && venv/bin/python manage.py shell << 'EOF'
from listings.models import Category
cat = Category.objects.get(slug='iepazisanas')
cat.icon = 'ti-hearts'
cat.save()
print(f'Ikona atjaunota: {cat.name} -> {cat.icon}')
EOF"""

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS)
_, stdout, stderr = ssh.exec_command(cmd)
print(stdout.read().decode())
ssh.close()
