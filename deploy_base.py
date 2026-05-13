import paramiko

HOST = '91.228.7.68'
USER = 'root'
PASS = 'F003xbFSplJyr44Z2B'
REMOTE = '/var/www/eizsole/templates/base.html'
LOCAL = r'C:\Users\USER\izsoles-platforma\templates\base.html'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS)

sftp = ssh.open_sftp()
sftp.put(LOCAL, REMOTE)
sftp.close()
print('base.html augšupielādēts')

_, stdout, stderr = ssh.exec_command('systemctl restart eizsole')
stdout.channel.recv_exit_status()
print('Serveris restartēts')

ssh.close()
print('Gatavs!')
