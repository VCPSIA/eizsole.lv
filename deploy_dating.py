import paramiko

HOST = '91.228.7.68'
USER = 'root'
PASS = 'F003xbFSplJyr44Z2B'

files = [
    (r'C:\Users\USER\izsoles-platforma\listings\models.py',             '/var/www/eizsole/listings/models.py'),
    (r'C:\Users\USER\izsoles-platforma\listings\views.py',              '/var/www/eizsole/listings/views.py'),
    (r'C:\Users\USER\izsoles-platforma\templates\listings\create.html', '/var/www/eizsole/templates/listings/create.html'),
    (r'C:\Users\USER\izsoles-platforma\templates\listings\category.html','/var/www/eizsole/templates/listings/category.html'),
]

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS)

sftp = ssh.open_sftp()
for local, remote in files:
    sftp.put(local, remote)
    print(f'OK: {remote}')
sftp.close()

cmds = [
    'cd /var/www/eizsole && venv/bin/python manage.py makemigrations listings',
    'cd /var/www/eizsole && venv/bin/python manage.py migrate',
    'systemctl restart eizsole',
]
for cmd in cmds:
    _, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode()
    err = stderr.read().decode()
    print(f'CMD: {cmd}')
    if out: print(out[:300])
    if err and 'warning' not in err.lower(): print('ERR:', err[:200])

ssh.close()
print('Gatavs!')
