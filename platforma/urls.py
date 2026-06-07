from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import RedirectView, TemplateView
from django.http import HttpResponse
from listings.sitemaps import ListingSitemap, CategorySitemap, StaticSitemap, AuctionSitemap, CitySitemap
from blog.sitemaps import BlogSitemap
from blog.urls import static_urlpatterns

sitemaps = {
    'listings':   ListingSitemap,
    'auctions':   AuctionSitemap,
    'categories': CategorySitemap,
    'static':     StaticSitemap,
    'cities':     CitySitemap,
    'blog':       BlogSitemap,
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
    path('blogs/', include('blog.urls')),
    path('', include((static_urlpatterns, 'pages'))),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('manifest.json', TemplateView.as_view(template_name='manifest.json', content_type='application/manifest+json')),
    path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/javascript')),
    path('offline/', TemplateView.as_view(template_name='offline.html'), name='offline'),
    path('BingSiteAuth.xml', lambda r: HttpResponse(
        '<?xml version="1.0"?>\n<users>\n\t<user>32FA50CBA8264DB505C818F1356C8977</user>\n</users>',
        content_type='application/xml'
    )),
    path('9ee765937c5ab780463252b28f1ae312.txt', lambda r: HttpResponse(
        '9ee765937c5ab780463252b28f1ae312',
        content_type='text/plain'
    )),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
