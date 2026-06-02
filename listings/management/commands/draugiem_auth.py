"""
Draugiem.lv autorizācija — izpildi vienu reizi lai iegūtu access_token.

Lietošana:
    python manage.py draugiem_auth

Pēc izpildes:
    1. Atver norādīto URL pārlūkā
    2. Pieteicies ar eizsole.lv Draugiem kontu
    3. Atļauj aplikācijai publicēt
    4. Nokopē 'token' no atgriestā URL
    5. Pievieno .env failā: DRAUGIEM_ACCESS_TOKEN=<token>
"""
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Draugiem.lv OAuth autorizācija'

    def handle(self, *args, **options):
        app_id  = settings.DRAUGIEM_APP_ID
        api_key = settings.DRAUGIEM_API_KEY

        if not app_id or not api_key:
            self.stdout.write(self.style.ERROR(
                '\nNav DRAUGIEM_APP_ID un DRAUGIEM_API_KEY!\n\n'
                'Soļi:\n'
                '1. Atver: https://www.draugiem.lv/applications/add/\n'
                '2. Izveido jaunu aplikāciju (nosaukums: eizsole.lv)\n'
                '3. Callback URL: https://eizsole.lv/social/draugiem/callback/\n'
                '4. Nokopē App ID un API Key\n'
                '5. Pievieno .env: DRAUGIEM_APP_ID=xxx DRAUGIEM_API_KEY=yyy\n'
                '6. Atkārtoti izpildi: python manage.py draugiem_auth\n'
            ))
            return

        auth_url = (
            f'https://api.draugiem.lv/authorize/'
            f'?app={app_id}'
            f'&redirect={settings.SITE_URL if hasattr(settings, "SITE_URL") else "https://eizsole.lv"}'
            f'/social/draugiem/callback/'
        )

        self.stdout.write(self.style.SUCCESS(
            f'\nDraugiem.lv autorizācija:\n\n'
            f'1. Atver šo URL pārlūkā:\n   {auth_url}\n\n'
            f'2. Pieteicies ar eizsole.lv Draugiem kontu\n'
            f'3. Atļauj aplikācijai publicēt\n'
            f'4. Pēc novirzīšanas URL redzēsi: ...?token=XXXXXX\n'
            f'5. Nokopē token un pievieno .env failā:\n'
            f'   DRAUGIEM_ACCESS_TOKEN=XXXXXX\n\n'
            f'Serverī izpildi:\n'
            f'   echo "DRAUGIEM_ACCESS_TOKEN=TOKEN" >> /var/www/eizsole/.env\n'
            f'   systemctl restart eizsole\n'
        ))
