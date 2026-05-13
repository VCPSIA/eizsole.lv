import paramiko

HOST = '91.228.7.68'
USER = 'root'
PASS = 'F003xbFSplJyr44Z2B'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS)

cmds = [
    'rm -f /var/www/eizsole/locale/en/LC_MESSAGES/django.mo',
    'rm -f /var/www/eizsole/locale/ru/LC_MESSAGES/django.mo',
    'rm -f /var/www/eizsole/locale/de/LC_MESSAGES/django.mo',
    'cd /var/www/eizsole && venv/bin/python manage.py compilemessages',
    'systemctl restart eizsole',
]

for cmd in cmds:
    _, stdout, stderr = ssh.exec_command(cmd)
    stdout.channel.recv_exit_status()
    out = stdout.read().decode(errors='replace')
    err = stderr.read().decode(errors='replace')
    print(f'OK: {cmd}')
    if out.strip(): print(out[:200])
    if err.strip() and 'warning' not in err.lower(): print('ERR:', err[:200])

ssh.close()
print('Gatavs!')
