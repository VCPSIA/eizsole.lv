import requests
import urllib3
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

INDEXNOW_KEY  = '9ee765937c5ab780463252b28f1ae312'
SITE_URL      = 'https://eizsole.lv'
INDEXNOW_URLS = [
    'https://www.bing.com/indexnow',
    'https://yandex.com/indexnow',
]


def _submit_indexnow(urls):
    """Iesniedz URL sarakstu IndexNow API."""
    payload = {
        'host':        'eizsole.lv',
        'key':         INDEXNOW_KEY,
        'keyLocation': f'{SITE_URL}/{INDEXNOW_KEY}.txt',
        'urlList':     urls[:100],
    }
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    for endpoint in INDEXNOW_URLS:
        try:
            requests.post(endpoint, json=payload, headers=headers,
                          timeout=8, verify=False)
        except Exception:
            pass


@receiver(post_save, sender='listings.Listing')
def listing_indexnow(sender, instance, created, **kwargs):
    """Kad sludinājums tiek apstiprināts — iesniedz IndexNow + sociālie."""
    if instance.moderation_status == 'approved' and instance.is_active:
        try:
            url = SITE_URL + reverse('listing_detail', args=[instance.pk])
            _submit_indexnow([url])
        except Exception:
            pass

        # Sociālie tīkli — tikai jauniem sludinājumiem
        if created:
            try:
                from .social_publishers import post_to_draugiem, post_to_facebook
                import threading
                threading.Thread(
                    target=lambda: (post_to_draugiem(instance),
                                   post_to_facebook(instance)),
                    daemon=True
                ).start()
            except Exception:
                pass


@receiver(post_save, sender='auctions.Auction')
def auction_indexnow(sender, instance, created, **kwargs):
    """Kad jauna izsole tiek izveidota — iesniedz IndexNow."""
    if created:
        try:
            url = SITE_URL + reverse('auction_detail', args=[instance.pk])
            _submit_indexnow([url])
        except Exception:
            pass
