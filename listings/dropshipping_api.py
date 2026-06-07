"""
Dropshipping API — XML un JSON eksports partneriem.
Pieeja: /dropshipping/feed.xml  vai  /dropshipping/feed.json
Autentifikācija: ?api_key=<atslega>  (iestatāma SiteSettings.dropshipping_api_key)
"""
import secrets
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from django.utils.xmlutils import SimplerXMLGenerator
from io import StringIO

from .models import DropshippingItem


def _check_api_key(request):
    key = request.GET.get('api_key') or request.headers.get('X-Api-Key', '')
    try:
        from .models import SiteSettings
        settings = SiteSettings.get()
        expected = getattr(settings, 'dropshipping_api_key', '')
        if not expected:
            return True  # Nav iestatīta — brīva piekļuve
        return secrets.compare_digest(key, expected)
    except Exception:
        return True


@require_GET
@csrf_exempt
def feed_xml(request):
    if not _check_api_key(request):
        return HttpResponse('Nepareiza API atslēga.', status=401)

    items = DropshippingItem.objects.filter(
        is_active=True,
        listing__is_active=True,
    ).select_related('listing', 'listing__category')

    out = StringIO()
    xml = SimplerXMLGenerator(out, 'utf-8')
    xml.startDocument()
    xml.startElement('products', {'xmlns': 'https://eizsole.lv/dropshipping/1.0'})

    for item in items:
        l = item.listing
        xml.startElement('product', {})
        def tag(name, val):
            xml.startElement(name, {})
            xml.characters(str(val) if val is not None else '')
            xml.endElement(name)
        tag('id', l.pk)
        tag('title', l.title)
        tag('description', l.description[:500] if l.description else '')
        tag('price', str(l.price) if l.price else '')
        tag('currency', 'EUR')
        tag('category', l.category.name if l.category else '')
        tag('condition', l.get_condition_display())
        tag('supplier', item.supplier_name)
        tag('supplier_price', str(item.supplier_price))
        tag('supplier_url', item.supplier_url or '')
        img = l.get_main_image()
        tag('image_url', request.build_absolute_uri(img.image.url) if img else '')
        tag('product_url', request.build_absolute_uri(f'/sludinajums/{l.pk}/'))
        tag('updated', str(l.updated_at.date()))
        xml.endElement('product')

    xml.endElement('products')
    return HttpResponse(out.getvalue(), content_type='application/xml; charset=utf-8')


@require_GET
@csrf_exempt
def feed_json(request):
    if not _check_api_key(request):
        return JsonResponse({'error': 'Nepareiza API atslēga.'}, status=401)

    items = DropshippingItem.objects.filter(
        is_active=True,
        listing__is_active=True,
    ).select_related('listing', 'listing__category')

    data = []
    for item in items:
        l = item.listing
        img = l.get_main_image()
        data.append({
            'id': l.pk,
            'title': l.title,
            'description': l.description[:500] if l.description else '',
            'price': str(l.price) if l.price else None,
            'currency': 'EUR',
            'category': l.category.name if l.category else '',
            'condition': l.get_condition_display(),
            'supplier': item.supplier_name,
            'supplier_price': str(item.supplier_price),
            'supplier_url': item.supplier_url or '',
            'image_url': request.build_absolute_uri(img.image.url) if img else '',
            'product_url': request.build_absolute_uri(f'/sludinajums/{l.pk}/'),
            'updated': str(l.updated_at.date()),
        })

    return JsonResponse({'count': len(data), 'products': data})
