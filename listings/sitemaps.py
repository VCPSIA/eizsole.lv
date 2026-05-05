from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Listing, Category


class ListingSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Listing.objects.filter(is_active=True, moderation_status='approved')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('listing_detail', args=[obj.pk])


class CategorySitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.6

    def items(self):
        return Category.objects.filter(parent__isnull=True)

    def location(self, obj):
        return reverse('category', args=[obj.slug])


class StaticSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return ['home', 'auction_list']

    def location(self, item):
        return reverse(item)
