import paramiko

HOST = '91.228.7.68'
USER = 'root'
PASS = 'F003xbFSplJyr44Z2B'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS)

_, stdout, stderr = ssh.exec_command('cd /var/www/eizsole && venv/bin/python manage.py compilemessages -v 2 2>&1')
out = stdout.read().decode(errors='replace')
print(out[:3000])
ssh.close()
