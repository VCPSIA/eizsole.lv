from django.core.mail import send_mail
from django.conf import settings
from .models import Notification


def notify(user, notif_type, text, url='', send_email=True):
    Notification.objects.create(user=user, notif_type=notif_type, text=text, url=url)
    if send_email and user.email:
        _send_email(user, text, url)


def _send_email(user, text, url=''):
    site_url = 'https://eizsole.lv'
    full_url = f'{site_url}{url}' if url else site_url
    display_name = getattr(user, 'first_name', '') or user.username

    body = (
        f'Sveiki, {display_name}!\n\n'
        f'{text}\n\n'
        f'{"Skatīt: " + full_url + chr(10) + chr(10) if url else ""}'
        f'— eizsole.lv komanda\n'
        f'{site_url}'
    )

    try:
        send_mail(
            subject=f'eizsole.lv — {text[:70]}',
            message=body,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@eizsole.lv'),
            recipient_list=[user.email],
            fail_silently=True,
        )
    except Exception:
        pass
