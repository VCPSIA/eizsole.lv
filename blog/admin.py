from django.contrib import admin
from django.utils.html import format_html
from .models import BlogPost, StaticPage


@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    list_display  = ('get_page_type_display', 'title_lv', 'is_published', 'updated_at')
    list_filter   = ('is_published',)
    fieldsets = (
        ('Lapas veids', {
            'fields': ('page_type', 'is_published'),
        }),
        ('Saturs — Latviski (LV)', {
            'fields': ('title_lv', 'content_lv'),
        }),
        ('Saturs — Krieviski (RU)', {
            'fields': ('title_ru', 'content_ru'),
            'classes': ('collapse',),
        }),
        ('Saturs — Angliski (EN)', {
            'fields': ('title_en', 'content_en'),
            'classes': ('collapse',),
        }),
        ('Saturs — Vāciski (DE)', {
            'fields': ('title_de', 'content_de'),
            'classes': ('collapse',),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        for field in ('content_lv', 'content_ru', 'content_en', 'content_de'):
            if field in form.base_fields:
                form.base_fields[field].widget.attrs.update({'rows': 20, 'style': 'font-family:monospace;font-size:.85rem'})
        return form


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display  = ('title', 'is_published', 'published_at')
    list_filter   = ('is_published',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'excerpt', 'content', 'image', 'author', 'is_published')}),
        ('SEO', {'fields': ('meta_description', 'meta_keywords'), 'classes': ('collapse',)}),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'content' in form.base_fields:
            form.base_fields['content'].widget.attrs.update({'rows': 25, 'style': 'font-family:monospace;font-size:.85rem'})
        return form
