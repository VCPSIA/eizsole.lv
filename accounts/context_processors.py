from .models import Notification


def notifications(request):
    if request.user.is_authenticated:
        unread = Notification.objects.filter(user=request.user, is_read=False).count()
        return {'unread_notifications': unread}
    return {'unread_notifications': 0}


def banners(request):
    try:
        from listings.models import Banner, SiteSettings, SidebarBanner
        settings = SiteSettings.get()
        if not settings.banner_enabled:
            rotating = []
            rotation_secs = 5
        else:
            qs = Banner.objects.filter(is_active=True).select_related('listing')
            rotating = [b for b in qs if b.listing is None or b.listing.is_active]
            rotation_secs = settings.banner_rotation_seconds
        sidebar = list(SidebarBanner.objects.filter(is_active=True).order_by('slot'))
        return {
            'active_banners': rotating,
            'banner_rotation_seconds': rotation_secs,
            'sidebar_banners': sidebar,
        }
    except Exception:
        return {'active_banners': [], 'banner_rotation_seconds': 5, 'sidebar_banners': []}
