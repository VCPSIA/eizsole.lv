import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'platforma.settings')
django.setup()

from accounts.sms import send_sms
send_sms('+37129266444', 'eizsole.lv tests: SMS darbojas!')
print('Nosutits!')
