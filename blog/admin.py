from django.contrib import admin
from .models import BlogPost


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
