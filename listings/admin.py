from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.db.models import Count
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages as admin_messages
from django.http import HttpResponse
from .models import Category, Listing, ListingImage, Report, Equipment, SiteSettings, DiscountCode, Banner, SidebarBanner, DropshippingItem, DropshippingSupplier, MatterhornConfig, MatterhornProduct


class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1


class DropshippingInline(admin.StackedInline):
    model = DropshippingItem
    extra = 0
    can_delete = True
    verbose_name = 'Dropshipping'
    verbose_name_plural = 'Dropshipping'
    fieldsets = [
        ('Piegādātājs', {
            'fields': ['is_active', 'supplier_name', 'supplier_url', 'supplier_price', 'supplier_contact'],
        }),
        ('Pasūtījuma izsekošana', {
            'fields': ['order_status', 'supplier_order_id', 'buyer_address', 'notes'],
            'classes': ['collapse'],
        }),
    ]


_LV = str.maketrans({'ā':'a','č':'c','ē':'e','ģ':'g','ī':'i','ķ':'k','ļ':'l','ņ':'n','š':'s','ū':'u','ž':'z'})

def _lv_key(text):
    return text.lower().translate(_LV)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'icon']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'slug']
    list_filter = ['parent']
    ordering = ['parent__name', 'name']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parent':
            field = super().formfield_for_foreignkey(db_field, request, **kwargs)
            cats = sorted(field.queryset, key=lambda c: _lv_key(c.name))
            field.choices = [('', '---------')] + [(c.pk, c.name) for c in cats]
            return field
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'category', 'price', 'is_auction', 'is_active', 'report_count', 'created_at']
    list_filter = ['is_auction', 'is_active', 'category', 'condition']
    search_fields = ['title', 'description']
    inlines = [ListingImageInline, DropshippingInline]
    actions = ['deactivate_listings', 'activate_listings']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(report_count=Count('reports'))

    def report_count(self, obj):
        count = obj.report_count
        if count > 0:
            return format_html('<span style="color:red;font-weight:bold">{}</span>', count)
        return count
    report_count.short_description = 'Ziņojumi'
    report_count.admin_order_field = 'report_count'

    @admin.action(description='Deaktivēt izvēlētos sludinājumus')
    def deactivate_listings(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} sludinājums(-i) deaktivēti.')

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'group', 'order']
    list_filter = ['group']
    ordering = ['group', 'order']

    @admin.action(description='Aktivēt izvēlētos sludinājumus')
    def activate_listings(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} sludinājums(-i) aktivēti.')


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Dropshipping API', {
            'fields': ['dropshipping_api_key'],
            'description': 'Feed URL: /dropshipping/feed.xml vai /dropshipping/feed.json — pievienot ?api_key=<atslega> ja aizpildīta.',
        }),
        ('Kontaktinformācija', {
            'fields': [
                'contact_company', 'contact_reg_nr', 'contact_email',
                'contact_phone', 'contact_address',
                'contact_facebook', 'contact_instagram', 'contact_twitter', 'contact_whatsapp',
            ],
            'description': 'Rādās lapas kājenē. Sociālo tīklu URL — ielikt pilno adresi (https://...).',
        }),
        ('Sludinājumu maksa', {
            'fields': ['listing_fee_enabled', 'listing_fee'],
            'description': 'Maksa, kas tiek novilkta no klienta maka, publicējot parasto sludinājumu.',
        }),
        ('Izsoles maksa', {
            'fields': ['auction_fee_enabled', 'auction_fee'],
            'description': 'Maksa, kas tiek novilkta no klienta maka, publicējot izsoli.',
        }),
        ('TOP sludinājums', {
            'fields': ['featured_listing_enabled', 'featured_listing_fee'],
            'description': 'Klients var samaksāt, lai sludinājums rādītos saraksta augšgalā, līdz kāds cits samaksā par TOP vietu.',
        }),
        ('TOP izsole', {
            'fields': ['featured_auction_enabled', 'featured_auction_fee'],
            'description': 'Klients var samaksāt, lai izsole rādītos saraksta augšgalā, līdz kāds cits samaksā par TOP vietu.',
        }),
        ('Galvenās lapas hero baneris', {
            'fields': ['hero_text_lv', 'hero_text_ru', 'hero_text_en', 'hero_text_de'],
            'description': 'Teksts, kas rādīsies uz galvenās lapas hero banera attēla. Var atstāt tukšu, ja tekstu nevēlas.',
        }),
        ('Reklāmas baneri', {
            'fields': ['banner_enabled', 'banner_fee', 'banner_rotation_seconds'],
            'description': 'Klients var samaksāt par reklāmas baneri, kas rotācijas kārtībā rādīsies visās lapas apakšlapās.',
        }),
        ('Centu izsoles', {
            'fields': [
                'cent_auction_enabled',
                'cent_auction_min_balance',
                'cent_auction_min_bid_increment',
                'cent_auction_commission_pct',
                'cent_auction_vat_pct',
            ],
            'description': (
                'Centu izsoles — izsoles ar ļoti zemām sākumcentām. '
                'Dalībai nepieciešams min. maka atlikums. '
                'Komisija (% + PVN) tiek atskaitīta no pārdevēja ieņēmumiem.'
            ),
        }),
    ]

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj, _ = SiteSettings.objects.get_or_create(pk=1)
        return super().changelist_view(request, extra_context)

    def get_queryset(self, request):
        SiteSettings.objects.get_or_create(pk=1)
        return super().get_queryset(request)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'listing', 'is_active', 'preview', 'created_at']
    list_filter = ['is_active']
    list_editable = ['is_active']
    search_fields = ['user__username', 'listing__title']
    readonly_fields = ['created_at', 'preview']
    fields = ['user', 'image', 'preview', 'text', 'link_url', 'is_active', 'created_at']

    def save_model(self, request, obj, form, change):
        if not obj.pk and not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px">', obj.image.url)
        return '—'
    preview.short_description = 'Priekšskatījums'


@admin.register(SidebarBanner)
class SidebarBannerAdmin(admin.ModelAdmin):
    list_display = ['slot', 'title', 'is_active', 'preview', 'link_url', 'updated_at']
    list_editable = ['is_active']
    ordering = ['slot']
    readonly_fields = ['preview']
    fields = ['slot', 'title', 'image', 'preview', 'link_url', 'is_active']

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:80px;max-width:200px;border-radius:6px;border:1px solid #dee2e6">', obj.image.url)
        return '—'
    preview.short_description = 'Priekšskatījums'

    def has_add_permission(self, request):
        return SidebarBanner.objects.count() < 3


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['listing', 'reason', 'reporter', 'status', 'created_at']
    list_filter = ['status', 'reason']
    search_fields = ['listing__title', 'reporter__username']
    readonly_fields = ['listing', 'reporter', 'reason', 'details', 'created_at']
    actions = ['mark_resolved', 'delete_reported_listing']

    @admin.action(description='Atzīmēt kā atrisinātu')
    def mark_resolved(self, request, queryset):
        queryset.update(status='resolved', resolved_by=request.user, resolved_at=timezone.now())
        self.message_user(request, f'{queryset.count()} ziņojums(-i) atzīmēti kā atrisināti.')

    @admin.action(description='Dzēst sludinājumu un atrisināt ziņojumus')
    def delete_reported_listing(self, request, queryset):
        listings = set(r.listing for r in queryset)
        for listing in listings:
            listing.delete()
        self.message_user(request, f'{len(listings)} sludinājums(-i) dzēsti.')


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'discount_value', 'used_count', 'max_uses', 'valid_until', 'is_active']
    list_editable = ['is_active']
    search_fields = ['code']
    list_filter = ['discount_type', 'is_active']
    readonly_fields = ['used_count']

    def get_urls(self):
        urls = super().get_urls()
        return [path('generēt/', self.admin_site.admin_view(self.generate_view), name='discountcode_generate')] + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['generate_url'] = 'admin:discountcode_generate'
        return super().changelist_view(request, extra_context=extra_context)

    def generate_view(self, request):
        import secrets, string, csv
        from decimal import Decimal

        ALPHABET = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789'  # bez 0/O/1/I/L

        def gen_code(prefix='', length=10):
            rand_len = length - len(prefix)
            return prefix + ''.join(secrets.choice(ALPHABET) for _ in range(rand_len))

        if request.method == 'POST':
            action = request.POST.get('action')

            try:
                discount_type  = request.POST['discount_type']
                discount_value = Decimal(request.POST['discount_value'])
                count          = min(int(request.POST.get('count', 1)), 500)
                prefix         = request.POST.get('prefix', '').strip().upper()[:6]
                valid_from_str = request.POST.get('valid_from', '').strip()
                valid_until_str = request.POST.get('valid_until', '').strip()
                is_active      = request.POST.get('is_active') == '1'
            except Exception:
                admin_messages.error(request, 'Nepareizi ievades dati.')
                return redirect('.')

            from django.utils.dateparse import parse_datetime
            valid_from  = parse_datetime(valid_from_str + ':00') if valid_from_str else None
            valid_until = parse_datetime(valid_until_str + ':00') if valid_until_str else None

            codes_made = []
            attempts = 0
            while len(codes_made) < count and attempts < count * 10:
                attempts += 1
                code = gen_code(prefix, length=max(8, 6 + len(prefix)))
                if not DiscountCode.objects.filter(code=code).exists():
                    obj = DiscountCode.objects.create(
                        code=code,
                        discount_type=discount_type,
                        discount_value=discount_value,
                        max_uses=1,
                        used_count=0,
                        valid_from=valid_from,
                        valid_until=valid_until,
                        is_active=is_active,
                    )
                    codes_made.append(obj)

            if action == 'download':
                response = HttpResponse(content_type='text/csv; charset=utf-8')
                response['Content-Disposition'] = f'attachment; filename="atlaidu-kodi-{len(codes_made)}.csv"'
                response.write('﻿')  # BOM for Excel
                w = csv.writer(response)
                w.writerow(['Kods', 'Veids', 'Vērtība', 'Derīgs no', 'Derīgs līdz'])
                for obj in codes_made:
                    label = f'{obj.discount_value}%' if obj.discount_type == 'percent' else f'€{obj.discount_value}'
                    w.writerow([obj.code, label, obj.discount_value,
                                obj.valid_from.strftime('%d.%m.%Y') if obj.valid_from else '',
                                obj.valid_until.strftime('%d.%m.%Y') if obj.valid_until else ''])
                return response

            admin_messages.success(request, f'Izveidoti {len(codes_made)} kodi.')
            return redirect('..')

        context = {
            **self.admin_site.each_context(request),
            'title': 'Ģenerēt atlaižu kodus',
            'opts': self.model._meta,
        }
        return render(request, 'admin/listings/discountcode/generate.html', context)


@admin.register(DropshippingItem)
class DropshippingAdmin(admin.ModelAdmin):
    list_display = ['listing_title', 'supplier_name', 'supplier_price', 'listing_price', 'profit_display', 'order_status', 'is_active', 'updated_at']
    list_filter  = ['order_status', 'is_active']
    search_fields = ['listing__title', 'supplier_name', 'supplier_order_id']
    list_editable = ['order_status']
    readonly_fields = ['profit_display', 'created_at', 'updated_at']
    fieldsets = [
        ('Sludinājums', {
            'fields': ['listing', 'is_active'],
        }),
        ('Piegādātājs', {
            'fields': ['supplier_name', 'supplier_url', 'supplier_price', 'supplier_contact'],
        }),
        ('Pasūtījuma izsekošana', {
            'fields': ['order_status', 'supplier_order_id', 'buyer_address', 'notes'],
        }),
        ('Info', {
            'fields': ['profit_display', 'created_at', 'updated_at'],
            'classes': ['collapse'],
        }),
    ]

    def listing_title(self, obj):
        return obj.listing.title[:60]
    listing_title.short_description = 'Sludinājums'

    def listing_price(self, obj):
        return f'€{obj.listing.price}' if obj.listing.price else '—'
    listing_price.short_description = 'Pārdošanas cena'

    def profit_display(self, obj):
        p = obj.profit
        if p is None:
            return '—'
        color = 'green' if p > 0 else 'red'
        return format_html('<strong style="color:{}">{} €</strong>', color, p)
    profit_display.short_description = 'Peļņa'


@admin.register(DropshippingSupplier)
class DropshippingSupplierAdmin(admin.ModelAdmin):
    list_display  = ['name', 'xml_feed_url', 'is_active', 'last_sync', 'import_btn']
    list_filter   = ['is_active']
    search_fields = ['name']
    readonly_fields = ['last_sync']
    fieldsets = [
        ('Piegādātājs', {'fields': ['name', 'is_active', 'notes']}),
        ('XML feed', {'fields': ['xml_feed_url'], 'description': 'URL uz piegādātāja XML produktu sarakstu.'}),
        ('API', {'fields': ['api_url', 'api_key'], 'classes': ['collapse']}),
        ('Sinhronizācija', {'fields': ['last_sync'], 'classes': ['collapse']}),
    ]

    def get_urls(self):
        urls = super().get_urls()
        custom = [path('<int:pk>/import/', self.admin_site.admin_view(self.import_xml_view), name='ds_import_xml')]
        return custom + urls

    def import_btn(self, obj):
        if obj.xml_feed_url:
            return format_html('<a class="button" href="{}import/">Importēt XML</a>', obj.pk)
        return '—'
    import_btn.short_description = 'Imports'

    def import_xml_view(self, request, pk):
        import urllib.request, xml.etree.ElementTree as ET
        from django.contrib.auth.models import User
        from django.utils import timezone as tz

        supplier = DropshippingSupplier.objects.get(pk=pk)
        if not supplier.xml_feed_url:
            self.message_user(request, 'Nav XML feed URL.', level='error')
            return redirect('..')

        try:
            with urllib.request.urlopen(supplier.xml_feed_url, timeout=15) as resp:
                raw = resp.read()
            root = ET.fromstring(raw)
        except Exception as e:
            self.message_user(request, f'Kļūda ielādējot XML: {e}', level='error')
            return redirect('..')

        admin_user = User.objects.filter(is_superuser=True).first()
        default_cat = Category.objects.filter(parent=None).first()
        created = updated = 0

        for prod in root.iter('product'):
            def g(tag, default=''):
                el = prod.find(tag)
                return el.text.strip() if el is not None and el.text else default

            title    = g('title') or g('name')
            price_s  = g('price') or g('retail_price')
            sup_price_s = g('supplier_price') or g('cost_price') or g('wholesale_price')
            desc     = g('description')
            img_url  = g('image_url') or g('image')
            sup_url  = g('url') or g('product_url') or g('link')
            ext_id   = g('id') or g('sku') or g('article')

            if not title:
                continue
            try:
                price = float(price_s.replace(',', '.')) if price_s else None
                sup_price = float(sup_price_s.replace(',', '.')) if sup_price_s else (price * 0.6 if price else 0)
            except Exception:
                price = None
                sup_price = 0

            from decimal import Decimal
            listing, was_created = Listing.objects.get_or_create(
                seller=admin_user,
                title=title,
                defaults={
                    'description': desc or title,
                    'category': default_cat,
                    'price': Decimal(str(price)) if price else None,
                    'condition': 'new',
                    'is_active': False,
                    'moderation_status': 'approved',
                }
            )
            ds, _ = DropshippingItem.objects.update_or_create(
                listing=listing,
                defaults={
                    'supplier_name': supplier.name,
                    'supplier_url': sup_url,
                    'supplier_price': Decimal(str(sup_price)),
                    'is_active': True,
                }
            )
            if was_created:
                created += 1
            else:
                updated += 1

        supplier.last_sync = tz.now()
        supplier.save(update_fields=['last_sync'])

        self.message_user(request, f'Imports pabeigts: {created} jauni, {updated} atjaunināti produkti.')
        return redirect('../..')


# ── MATTERHORN ──────────────────────────────────────────────────

@admin.register(MatterhornConfig)
class MatterhornConfigAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Savienojums', {
            'fields': ['xml_feed_url', 'api_key', 'api_username', 'api_password'],
            'description': 'Matterhorn B2B API atslēga vai lietotājvārds/parole. API key tiek pievienots kā Authorization: Bearer <key> headeris.',
        }),
        ('Cenu uzstādījumi', {
            'fields': ['markup_percent', 'default_category'],
            'description': 'Uzcenojums virs Matterhorn vairumcenas. Noklusējuma kategorija jauniem produktiem.',
        }),
        ('Sinhronizācija', {
            'fields': ['sync_enabled', 'last_sync', 'sync_log'],
        }),
    ]
    readonly_fields = ['last_sync', 'sync_log']

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path('sync-now/',    self.admin_site.admin_view(self.sync_now_view),    name='matterhorn_sync_now'),
            path('delete-all/',  self.admin_site.admin_view(self.delete_all_view),  name='matterhorn_delete_all'),
        ]
        return custom + urls

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['sync_url']       = '../sync-now/'
        extra_context['delete_all_url'] = '../delete-all/'
        return super().changeform_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        MatterhornConfig.get()
        extra_context = extra_context or {}
        extra_context['delete_all_url'] = 'delete-all/'
        return super().changelist_view(request, extra_context)

    def sync_now_view(self, request):
        from listings.matterhorn_sync import run_sync
        config = MatterhornConfig.get()
        created, updated, errors = run_sync(config, limit=None)
        if isinstance(errors, str):
            self.message_user(request, f'Kļūda: {errors}', level='error')
        else:
            self.message_user(request, f'Matterhorn sync pabeigts: {created} jauni, {updated} atjaunināti, {errors} kļūdas.', level='success')
        return redirect('../')

    def delete_all_view(self, request):
        mp_qs = MatterhornProduct.objects.all()
        listing_ids = list(mp_qs.filter(listing__isnull=False).values_list('listing_id', flat=True))
        mp_count = mp_qs.count()
        mp_qs.delete()
        from listings.models import Listing as L
        L.objects.filter(pk__in=listing_ids).delete()
        self.message_user(request,
            f'Dzēsti {mp_count} Matterhorn produkti un {len(listing_ids)} sludinājumi.',
            level='success')
        return redirect('../')

    def has_add_permission(self, request):
        return not MatterhornConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        MatterhornConfig.get()
        return super().changelist_view(request, extra_context)


@admin.register(MatterhornProduct)
class MatterhornProductAdmin(admin.ModelAdmin):
    list_display  = ['name', 'brand', 'wholesale_price', 'retail_price', 'total_stock_display', 'is_active', 'listing_link', 'last_updated']
    list_filter   = ['is_active', 'brand', 'currency']
    search_fields = ['name', 'brand', 'matterhorn_id', 'category_path']
    readonly_fields = ['matterhorn_id', 'last_updated', 'created_at', 'sizes_stock_display', 'ean_list', 'images_preview']
    list_editable = ['is_active']
    list_per_page = 50
    actions = ['delete_with_listings']

    @admin.action(description='🗑 Dzēst izvēlētos + to sludinājumus')
    def delete_with_listings(self, request, queryset):
        listing_ids = list(queryset.filter(listing__isnull=False).values_list('listing_id', flat=True))
        n = queryset.count()
        queryset.delete()
        from listings.models import Listing as L
        L.objects.filter(pk__in=listing_ids).delete()
        self.message_user(request, f'Dzēsti {n} produkti un {len(listing_ids)} sludinājumi.')
    fieldsets = [
        ('Produkts', {'fields': ['matterhorn_id', 'name', 'brand', 'description', 'category_path', 'product_url', 'is_active']}),
        ('Cenas', {'fields': ['wholesale_price', 'retail_price', 'currency']}),
        ('Vizuālie', {'fields': ['images_preview', 'colors']}),
        ('Izmēri un krājumi', {'fields': ['sizes_stock_display']}),
        ('EAN kodi', {'fields': ['ean_list']}),
        ('Sludinājums', {'fields': ['listing']}),
        ('Meta', {'fields': ['last_updated', 'created_at'], 'classes': ['collapse']}),
    ]

    def total_stock_display(self, obj):
        s = obj.total_stock
        color = 'green' if s > 0 else 'red'
        return format_html('<span style="color:{}">{}</span>', color, s)
    total_stock_display.short_description = 'Krājumi'

    def listing_link(self, obj):
        if obj.listing:
            return format_html('<a href="/sludinajums/{}/" target="_blank">#{}</a>', obj.listing.pk, obj.listing.pk)
        return '—'
    listing_link.short_description = 'Sludinājums'

    def sizes_stock_display(self, obj):
        if not obj.sizes_stock:
            return '—'
        rows = ''.join(
            f'<tr><td style="padding:2px 8px">{sz}</td>'
            f'<td style="padding:2px 8px">{v.get("stock",0)}</td>'
            f'<td style="padding:2px 8px;color:#666">{v.get("ean","")}</td></tr>'
            for sz, v in obj.sizes_stock.items()
        )
        return format_html('<table><tr><th>Izmērs</th><th>Krājums</th><th>EAN</th></tr>{}</table>', rows)
    sizes_stock_display.short_description = 'Izmēri un krājumi'

    def ean_list(self, obj):
        return ', '.join(obj.ean_codes) if obj.ean_codes else '—'
    ean_list.short_description = 'EAN kodi'

    def images_preview(self, obj):
        if not obj.image_urls:
            return '—'
        imgs = ''.join(
            f'<img src="{url}" style="height:60px;border-radius:4px;margin:2px">'
            for url in obj.image_urls[:5]
        )
        return format_html(imgs)
    images_preview.short_description = 'Attēli'
