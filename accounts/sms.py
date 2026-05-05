from django.conf import settings


def send_sms(phone, message):
    """
    Sūta SMS. Dev režīmā drukā konsolē.
    Produkcijā — konfigurē TWILIO_* settings.py vai izmanto citu pakalpojumu.
    """
    if getattr(settings, 'TWILIO_ACCOUNT_SID', None):
        _send_via_twilio(phone, message)
    else:
        # Dev režīms — izdrukā konsolē
        print(f'\n{"="*50}')
        print(f'SMS uz {phone}:')
        print(f'{message}')
        print(f'{"="*50}\n')


def _send_via_twilio(phone, message):
    try:
        from twilio.rest import Client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=message,
            from_=settings.TWILIO_FROM_NUMBER,
            to=phone,
        )
    except Exception as e:
        print(f'SMS kļūda: {e}')
