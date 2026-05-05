"""
AI bilžu moderācija ar Claude claude-haiku-4-5.
Pārbauda: pornogrāfisks saturs, politisks saturs, vardarbība.
Ja API atslēga nav iestatīta — visi sludinājumi automātiski apstiprināti.
"""
import base64
import json
import logging
from pathlib import Path
from django.conf import settings

logger = logging.getLogger(__name__)

PROMPT = """Analizē šo attēlu un pārbaudi vai tajā ir nevēlams saturs.

Pārbaudi šādas kategorijas:
1. Pornogrāfisks vai seksuāli eksplicīts saturs
2. Politiskā propaganda, politiski simboli vai politisks saturs
3. Vardarbīgs vai šokējošs saturs
4. Naida runa (rasistiski simboli, u.c.)

Atbildi TIKAI ar JSON formātā (bez citiem tekstiem):
{"safe": true/false, "reason": "iemesls latviešu valodā ja nav droši, vai null ja droši", "category": "categorija ja nav droši vai null"}

Esi konservatīvs — ja esi nedrošs, atbildi safe: false."""


def _get_media_type(file_path: str) -> str:
    ext = Path(file_path).suffix.lower()
    return {
        '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
        '.png': 'image/png', '.gif': 'image/gif',
        '.webp': 'image/webp',
    }.get(ext, 'image/jpeg')


def check_image(image_path: str) -> dict:
    """
    Pārbauda vienu bildi.
    Atgriež: {'safe': bool, 'reason': str|None, 'category': str|None}
    """
    api_key = getattr(settings, 'ANTHROPIC_API_KEY', None)
    if not api_key:
        return {'safe': True, 'reason': None, 'category': None}

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)

        with open(image_path, 'rb') as f:
            data = base64.standard_b64encode(f.read()).decode()

        media_type = _get_media_type(image_path)

        response = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=256,
            messages=[{
                'role': 'user',
                'content': [
                    {
                        'type': 'image',
                        'source': {
                            'type': 'base64',
                            'media_type': media_type,
                            'data': data,
                        },
                    },
                    {'type': 'text', 'text': PROMPT},
                ],
            }],
        )

        text = response.content[0].text.strip()
        # Atrod JSON bloku
        start = text.find('{')
        end = text.rfind('}') + 1
        result = json.loads(text[start:end])
        return {
            'safe': bool(result.get('safe', True)),
            'reason': result.get('reason'),
            'category': result.get('category'),
        }

    except Exception as e:
        logger.warning(f'AI moderācija neizdevās ({image_path}): {e}')
        # Kļūdas gadījumā — pieļauj publicēšanu (lai neblokētu lietotājus)
        return {'safe': True, 'reason': None, 'category': None}


def check_listing_images(listing) -> dict:
    """
    Pārbauda visas sludinājuma bildes.
    Atgriež: {'safe': bool, 'flags': list[dict]}
    """
    flags = []
    for img in listing.images.all():
        try:
            path = img.image.path
            result = check_image(path)
            if not result['safe']:
                flags.append({
                    'image': img.pk,
                    'reason': result.get('reason', 'Nepiemērots saturs'),
                    'category': result.get('category', 'nezināms'),
                })
        except Exception as e:
            logger.warning(f'Nevar pārbaudīt bildi {img.pk}: {e}')

    return {
        'safe': len(flags) == 0,
        'flags': flags,
    }
