from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.db.models import Count
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages as admin_messages
from django.http import HttpResponse
from .models import Category, Listing, ListingImage, Report, Equipment, SiteSettings, DiscountCode, Banner, SidebarBanner


class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1


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
    inlines = [ListingImageInline]
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
        ('Reklāmas baneri', {
            'fields': ['banner_enabled', 'banner_fee', 'banner_rotation_seconds'],
            'description': 'Klients var samaksāt par reklāmas baneri, kas rotācijas kārtībā rādīsies visās lapas apakšlapās.',
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
