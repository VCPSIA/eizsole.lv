import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'platforma.settings')
django.setup()

from accounts.models import PhoneVerification

latest = PhoneVerification.objects.order_by('-created_at')[:5]
for v in latest:
    print(f'{v.user.username} | {v.phone} | kods:{v.code} | derīgs:{v.is_valid()} | izmantots:{v.is_used}')
