"""
Matterhorn XML importētājs.
Atbalsta Matterhorn izvērsto XML formātu:
- Produkta info (nosaukums, apraksts, zīmols, izmēri)
- Neto vairumcenas
- Attēlu saites
- Krājumi pa izmēriem
- EAN kodi
- Krāsas
"""
import urllib.request, urllib.error
import xml.etree.ElementTree as ET
import logging
from decimal import Decimal, InvalidOperation
from django.utils import timezone
from django.contrib.auth.models import User

log = logging.getLogger(__name__)


def _text(el, tag, default=''):
    node = el.find(tag)
    return (node.text or '').strip() if node is not None else default


def _decimal(val, default=Decimal('0')):
    try:
        return Decimal(str(val).replace(',', '.').strip())
    except (InvalidOperation, ValueError):
        return default


def _fetch_xml(url, username='', password=''):
    req = urllib.request.Request(url)
    if username:
        import base64
        creds = base64.b64encode(f'{username}:{password}'.encode()).decode()
        req.add_header('Authorization', f'Basic {creds}')
    req.add_header('User-Agent', 'eizsole.lv/1.0')
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def _parse_product(prod_el):
    """Parsē vienu <product> elementu → dict."""
    p = {}

    # ID
    p['id'] = (
        _text(prod_el, 'id') or
        _text(prod_el, 'product_id') or
        _text(prod_el, 'sku') or
        prod_el.get('id', '')
    )

    # Pamata lauki
    p['name']        = _text(prod_el, 'name') or _text(prod_el, 'title')
    p['brand']       = _text(prod_el, 'brand') or _text(prod_el, 'manufacturer')
    p['description'] = _text(prod_el, 'description') or _text(prod_el, 'long_description')
    p['category']    = _text(prod_el, 'category') or _text(prod_el, 'category_path')
    p['product_url'] = _text(prod_el, 'url') or _text(prod_el, 'product_url') or _text(prod_el, 'link')

    # Cenas — meklē vairākus iespējamos tagus
    wholesale_raw = (
        _text(prod_el, 'wholesale_price') or
        _text(prod_el, 'net_price') or
        _text(prod_el, 'price_net') or
        _text(prod_el, 'netto_price') or
        _text(prod_el, 'purchase_price') or
        _text(prod_el, 'price')
    )
    p['wholesale_price'] = _decimal(wholesale_raw)

    retail_raw = (
        _text(prod_el, 'retail_price') or
        _text(prod_el, 'suggested_price') or
        _text(prod_el, 'price_gross') or
        _text(prod_el, 'msrp')
    )
    p['retail_price'] = _decimal(retail_raw)
    p['currency']    = _text(prod_el, 'currency') or 'EUR'

    # Attēli — dažādas struktūras
    images = []
    for tag in ('images', 'photos', 'gallery'):
        imgs_el = prod_el.find(tag)
        if imgs_el is not None:
            for img in imgs_el:
                url = img.text or img.get('url') or img.get('src') or ''
                if url.strip():
                    images.append(url.strip())
    # Arī tiešie <image> tagi
    for img_el in prod_el.findall('image'):
        url = img_el.text or img_el.get('url') or ''
        if url.strip():
            images.append(url.strip())
    p['image_urls'] = images[:10]

    # Izmēri, krājumi, EAN
    sizes = {}
    eans  = []
    for tag in ('variants', 'sizes', 'stocks', 'stock'):
        variants_el = prod_el.find(tag)
        if variants_el is not None:
            for v in variants_el:
                size  = _text(v, 'size') or _text(v, 'size_name') or v.get('size', '')
                stock = int(_decimal(_text(v, 'stock') or _text(v, 'quantity') or v.get('stock', '0')))
                ean   = _text(v, 'ean') or _text(v, 'barcode') or v.get('ean', '')
                if size:
                    sizes[size] = {'stock': stock, 'ean': ean}
                if ean and ean not in eans:
                    eans.append(ean)
    p['sizes_stock'] = sizes
    p['ean_codes']   = eans

    # Krāsas
    colors = []
    colors_el = prod_el.find('colors')
    if colors_el is None:
        colors_el = prod_el.find('colour')
    if colors_el is not None:
        for c in colors_el:
            name = c.text or c.get('name') or ''
            if name.strip():
                colors.append(name.strip())
    else:
        color = _text(prod_el, 'color') or _text(prod_el, 'colour')
        if color:
            colors.append(color)
    p['colors'] = colors

    return p


def run_sync(config=None, limit=None):
    """
    Galvenā sinhronizācijas funkcija.
    Atgriež (izveidoti, atjaunināti, kļūdas) skaitu.
    """
    from .models import MatterhornConfig, MatterhornProduct, Listing, DropshippingItem, Category

    if config is None:
        config = MatterhornConfig.get()

    if not config.xml_feed_url:
        return 0, 0, 'Nav XML feed URL.'

    # Lejupielādē XML
    try:
        raw = _fetch_xml(config.xml_feed_url, config.api_username, config.api_password)
    except Exception as e:
        msg = f'Kļūda ielādējot XML: {e}'
        log.error(msg)
        return 0, 0, msg

    # Parsē XML
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        msg = f'XML parsēšanas kļūda: {e}'
        log.error(msg)
        return 0, 0, msg

    # Atrast produktu elementus (dažādi iespējamie tagnames)
    products = (
        root.findall('product') or
        root.findall('.//product') or
        root.findall('item') or
        root.findall('.//item')
    )

    admin_user = User.objects.filter(is_superuser=True).first()
    default_cat = config.default_category or Category.objects.filter(parent=None).first()
    markup = config.markup_percent / Decimal('100')

    created = updated = errors = 0

    for i, prod_el in enumerate(products):
        if limit and i >= limit:
            break
        try:
            data = _parse_product(prod_el)
            if not data['id'] or not data['name']:
                continue

            # Aprēķina pārdošanas cenu
            if data['retail_price'] > 0:
                sell_price = data['retail_price']
            elif data['wholesale_price'] > 0:
                sell_price = (data['wholesale_price'] * (1 + markup)).quantize(Decimal('0.01'))
            else:
                sell_price = None

            mp, was_created = MatterhornProduct.objects.update_or_create(
                matterhorn_id=data['id'],
                defaults={
                    'name':           data['name'],
                    'brand':          data['brand'],
                    'description':    data['description'],
                    'category_path':  data['category'],
                    'wholesale_price': data['wholesale_price'],
                    'retail_price':   sell_price or Decimal('0'),
                    'currency':       data['currency'],
                    'image_urls':     data['image_urls'],
                    'sizes_stock':    data['sizes_stock'],
                    'ean_codes':      data['ean_codes'],
                    'colors':         data['colors'],
                    'product_url':    data['product_url'],
                    'is_active':      True,
                }
            )

            # Izveido vai atjaunina sludinājumu
            total_stock = sum(v.get('stock', 0) for v in data['sizes_stock'].values()) if data['sizes_stock'] else 1
            if mp.listing is None and admin_user and sell_price:
                sizes_text = ', '.join(data['sizes_stock'].keys()) if data['sizes_stock'] else ''
                desc_parts = [data['description'] or data['name']]
                if data['brand']:
                    desc_parts.append(f'Zīmols: {data["brand"]}')
                if sizes_text:
                    desc_parts.append(f'Pieejamie izmēri: {sizes_text}')
                if data['colors']:
                    desc_parts.append(f'Krāsas: {", ".join(data["colors"])}')
                if data['ean_codes']:
                    desc_parts.append(f'EAN: {", ".join(data["ean_codes"][:3])}')

                listing = Listing.objects.create(
                    title=f'{data["brand"]} {data["name"]}'.strip() if data['brand'] else data['name'],
                    description='\n'.join(desc_parts),
                    category=default_cat,
                    seller=admin_user,
                    price=sell_price,
                    condition='new',
                    is_active=total_stock > 0,
                    moderation_status='approved',
                    reference_url=data['product_url'],
                )
                mp.listing = listing
                mp.save(update_fields=['listing'])

                DropshippingItem.objects.get_or_create(
                    listing=listing,
                    defaults={
                        'supplier_name':  'Matterhorn',
                        'supplier_url':   data['product_url'],
                        'supplier_price': data['wholesale_price'],
                        'is_active':      True,
                    }
                )
            elif mp.listing:
                # Atjaunina esošo sludinājumu
                mp.listing.price     = sell_price or mp.listing.price
                mp.listing.is_active = total_stock > 0
                mp.listing.save(update_fields=['price', 'is_active'])

            if was_created:
                created += 1
            else:
                updated += 1

        except Exception as e:
            log.exception(f'Kļūda apstrādājot produktu: {e}')
            errors += 1

    # Saglabā sinhronizācijas laiku
    config.last_sync = timezone.now()
    config.sync_log  = (
        f'{config.last_sync.strftime("%d.%m.%Y %H:%M")} — '
        f'Jauni: {created}, Atjaunināti: {updated}, Kļūdas: {errors}'
    )
    config.save(update_fields=['last_sync', 'sync_log'])

    return created, updated, errors
