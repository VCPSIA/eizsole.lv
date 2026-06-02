from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from .models import Listing, Category
from auctions.models import Auction


class ListingSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Listing.objects.filter(is_active=True, moderation_status='approved').order_by('-updated_at')

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


class AuctionSitemap(Sitemap):
    changefreq = 'hourly'
    priority = 0.9

    def items(self):
        return Auction.objects.filter(is_finished=False, ends_at__gt=timezone.now()).order_by('ends_at')

    def lastmod(self, obj):
        return obj.ends_at

    def location(self, obj):
        return reverse('auction_detail', args=[obj.pk])


class StaticSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return ['home', 'auction_list']

    def location(self, item):
        return reverse(item)


class CitySitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.7

    def items(self):
        from .views import CITY_SLUGS
        return list(CITY_SLUGS.keys())

    def location(self, city_slug):
        return reverse('city_listings', args=[city_slug])
