from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import RedirectView, TemplateView
from listings.sitemaps import ListingSitemap, CategorySitemap, StaticSitemap, AuctionSitemap

sitemaps = {
    'listings': ListingSitemap,
    'auctions': AuctionSitemap,
    'categories': CategorySitemap,
    'static': StaticSitemap,
}

urlpatterns = [
    path('eizsole-panelis-2026/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('listings.urls')),
    path('accounts/', include('accounts.urls')),
    path('_/login/', RedirectView.as_view(url='/accounts/login/'), name='account_login'),
    path('_/signup/', RedirectView.as_view(url='/accounts/register/'), name='account_signup'),
    path('social/', include('allauth.socialaccount.urls')),
    path('', include('allauth.socialaccount.providers.google.urls')),
    path('', include('allauth.socialaccount.providers.facebook.urls')),
    path('izsoles/', include('auctions.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('manifest.json', TemplateView.as_view(template_name='manifest.json', content_type='application/manifest+json')),
    path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/javascript')),
    path('offline/', TemplateView.as_view(template_name='offline.html'), name='offline'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
