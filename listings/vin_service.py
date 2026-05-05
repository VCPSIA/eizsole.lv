"""
vehiclehistory.app API integrācija.
Iestatīt VEHICLEHISTORY_API_KEY settings.py vai .env.
Ja atslēga nav iestatīta — atgriež demo datus.
"""
import json
import urllib.request
import urllib.error
from django.conf import settings

API_BASE = 'https://api.vehiclehistory.app'

DEMO_REPORT = {
    '_demo': True,
    'vin': 'DEMO',
    'make': 'Demo Marka',
    'model': 'Demo Modelis',
    'year': 2019,
    'engine': '2.0 TDI',
    'color': 'Melns',
    'country_of_origin': 'DE',
    'mileage_records': [
        {'date': '2020-03-15', 'mileage': 25000, 'source': 'Tehniskā apskate'},
        {'date': '2021-08-22', 'mileage': 61000, 'source': 'Tehniskā apskate'},
        {'date': '2023-01-10', 'mileage': 98000, 'source': 'Serviss'},
    ],
    'accidents': [],
    'owners_count': 2,
    'theft': False,
    'write_off': False,
    'last_inspection': '2024-11-01',
    'inspection_valid': True,
}


def fetch_report(vin: str) -> dict:
    """
    Izsauc vehiclehistory.app API.
    Atgriež dict ar datiem vai {'error': '...'}.
    """
    api_key = getattr(settings, 'VEHICLEHISTORY_API_KEY', '')
    if not api_key:
        demo = dict(DEMO_REPORT)
        demo['vin'] = vin
        return demo

    url = f'{API_BASE}/v2/report/{vin.upper()}'
    req = urllib.request.Request(url, headers={
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json',
        'User-Agent': 'eizsole-lv/1.0',
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        try:
            err = json.loads(body)
            return {'error': err.get('message', f'HTTP {e.code}')}
        except Exception:
            return {'error': f'HTTP {e.code}'}
    except Exception as e:
        return {'error': str(e)}
