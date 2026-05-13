import paramiko

HOST = '91.228.7.68'
USER = 'root'
PASS = 'F003xbFSplJyr44Z2B'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PASS)

# Check if .mo files exist and their sizes
_, stdout, _ = ssh.exec_command(
    'ls -la /var/www/eizsole/locale/en/LC_MESSAGES/ '
    '/var/www/eizsole/locale/ru/LC_MESSAGES/ '
    '/var/www/eizsole/locale/de/LC_MESSAGES/ 2>&1'
)
print(stdout.read().decode(errors='replace'))

# Try compiling just our project files
_, stdout, stderr = ssh.exec_command(
    'cd /var/www/eizsole && venv/bin/python manage.py compilemessages -l en -l ru -l de -v 2 2>&1'
)
out = stdout.read().decode(errors='replace')
err = stderr.read().decode(errors='replace')
print("STDOUT:", out[:2000])
print("STDERR:", err[:2000])

ssh.close()
