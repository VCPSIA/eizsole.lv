from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from listings.sitemaps import ListingSitemap, CategorySitemap, StaticSitemap

sitemaps = {
    'listings': ListingSitemap,
    'categories': CategorySitemap,
    'static': StaticSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('listings.urls')),
    path('accounts/', include('accounts.urls')),
    path('izsoles/', include('auctions.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
