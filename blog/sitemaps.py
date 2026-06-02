from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import BlogPost


class BlogSitemap(Sitemap):
    changefreq = 'monthly'
    priority   = 0.6

    def items(self):
        return BlogPost.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('blog_detail', args=[obj.slug])
