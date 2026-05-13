import paramiko

HOST = '91.228.7.68'
USER = 'root'
PASS = 'F003xbFSplJyr44Z2B'

files = [
    (r'C:\Users\USER\izsoles-platforma\locale\en\LC_MESSAGES\django.po', '/var/www/eizsole/locale/en/LC_MESSAGES/django.po'),
    (r'C:\Users\USER\izsoles-platforma\locale\ru\LC_MESSAGES\django.po', '/var/www/eizsole/locale/ru/LC_MESSAGES/django.po'),
    (r'C:\Users\USER\izsoles-platforma\locale\de\LC_MESSAGES\django.po', '/var/www/eizsole/locale/de/LC_MESSAGES/django.po'),
]

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS)

sftp = ssh.open_sftp()
for local, remote in files:
    sftp.put(local, remote)
    print(f'Augšupielādēts: {remote}')
sftp.close()

cmds = [
    'cd /var/www/eizsole && venv/bin/python manage.py compilemessages',
    'systemctl restart eizsole',
]
for cmd in cmds:
    _, stdout, stderr = ssh.exec_command(cmd)
    stdout.channel.recv_exit_status()
    print(f'OK: {cmd}')

ssh.close()
print('Gatavs!')
