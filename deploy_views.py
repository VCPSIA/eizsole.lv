import paramiko

HOST = '91.228.7.68'
USER = 'root'
PASS = 'F003xbFSplJyr44Z2B'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS)

sftp = ssh.open_sftp()
sftp.put(r'C:\Users\USER\izsoles-platforma\listings\views.py', '/var/www/eizsole/listings/views.py')
print('OK: views.py')
sftp.close()

_, stdout, _ = ssh.exec_command('systemctl restart eizsole')
stdout.channel.recv_exit_status()
print('Restartēts')
ssh.close()
