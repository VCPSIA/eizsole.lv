"""
Auto-publicēšana sociālajos tīklos — Draugiem.lv un Facebook.
Katru reizi kad sludinājums tiek apstiprināts, tas tiek publicēts.
"""
import requests
import urllib3
import logging

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = logging.getLogger(__name__)

SITE_URL = 'https://eizsole.lv'


# ── DRAUGIEM.LV ──────────────────────────────────────────────────────────────

DRAUGIEM_API = 'https://api.draugiem.lv/json/'


def post_to_draugiem(listing):
    """Publicē sludinājumu Draugiem.lv uzņēmuma lapā."""
    from django.conf import settings

    app_id       = getattr(settings, 'DRAUGIEM_APP_ID', '')
    api_key      = getattr(settings, 'DRAUGIEM_API_KEY', '')
    access_token = getattr(settings, 'DRAUGIEM_ACCESS_TOKEN', '')

    if not all([app_id, api_key, access_token]):
        return False

    url = f'{SITE_URL}/sludinajums/{listing.pk}/'
    img = listing.get_main_image()

    text = (
        f'{listing.title}\n\n'
        f'{listing.description[:200].strip()}...\n\n'
        f'{"€" + str(listing.price) if listing.price else "Pēc vienošanās"} | '
        f'{listing.city or listing.location or ""}\n\n'
        f'🔗 {url}'
    )

    params = {
        'app':          app_id,
        'apikey':       api_key,
        'action':       'post_add',
        'token':        access_token,
        'text':         text,
        'url':          url,
        'url_title':    listing.title,
        'url_desc':     listing.description[:150],
    }
    if img:
        params['url_image'] = f'{SITE_URL}{img.image.url}'

    try:
        r = requests.get(DRAUGIEM_API, params=params, timeout=10, verify=False)
        data = r.json() if r.content else {}
        if data.get('status') == 'OK' or r.status_code == 200:
            logger.info(f'Draugiem OK: {listing.title}')
            return True
        else:
            logger.warning(f'Draugiem klude: {data}')
            return False
    except Exception as e:
        logger.error(f'Draugiem exception: {e}')
        return False


# ── FACEBOOK ─────────────────────────────────────────────────────────────────

FB_API = 'https://graph.facebook.com/v19.0'


def post_to_facebook(listing):
    """Publicē sludinājumu Facebook lapā."""
    from django.conf import settings

    page_id    = getattr(settings, 'FACEBOOK_PAGE_ID', '')
    page_token = getattr(settings, 'FACEBOOK_PAGE_TOKEN', '')

    if not all([page_id, page_token]):
        return False

    url = f'{SITE_URL}/sludinajums/{listing.pk}/'
    img = listing.get_main_image()

    message = (
        f'🆕 {listing.title}\n\n'
        f'{listing.description[:300].strip()}...\n\n'
        f'{"💶 €" + str(listing.price) if listing.price else "💬 Pēc vienošanās"}'
        f'{" | 📍 " + listing.city if listing.city else ""}\n\n'
        f'👉 Skaties: {url}'
    )

    try:
        if img:
            # Publicē ar attēlu
            endpoint = f'{FB_API}/{page_id}/photos'
            data = {
                'url':          f'{SITE_URL}{img.image.url}',
                'caption':      message,
                'access_token': page_token,
            }
        else:
            # Publicē bez attēla
            endpoint = f'{FB_API}/{page_id}/feed'
            data = {
                'message':      message,
                'link':         url,
                'access_token': page_token,
            }

        r = requests.post(endpoint, data=data, timeout=15, verify=False)
        result = r.json()
        if 'id' in result:
            logger.info(f'Facebook OK: {listing.title} → {result["id"]}')
            return True
        else:
            logger.warning(f'Facebook klude: {result}')
            return False
    except Exception as e:
        logger.error(f'Facebook exception: {e}')
        return False
