import paramiko

HOST = '91.228.7.68'
USER = 'root'
PASS = 'F003xbFSplJyr44Z2B'

files = [
    (r'C:\Users\USER\izsoles-platforma\listings\sitemaps.py', '/var/www/eizsole/listings/sitemaps.py'),
    (r'C:\Users\USER\izsoles-platforma\platforma\urls.py', '/var/www/eizsole/platforma/urls.py'),
]

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS)

sftp = ssh.open_sftp()
for local, remote in files:
    sftp.put(local, remote)
    print(f'Augšupielādēts: {remote}')
sftp.close()

_, stdout, stderr = ssh.exec_command('systemctl restart eizsole')
stdout.channel.recv_exit_status()
print('Serveris restartēts')

ssh.close()
print('Gatavs!')
