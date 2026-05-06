from .models import Notification


def notifications(request):
    if request.user.is_authenticated:
        unread = Notification.objects.filter(user=request.user, is_read=False).count()
        return {'unread_notifications': unread}
    return {'unread_notifications': 0}


def banners(request):
    try:
        from listings.models import Banner, SiteSettings
        settings = SiteSettings.get()
        if not settings.banner_enabled:
            return {'active_banners': [], 'banner_rotation_seconds': 5}
        qs = Banner.objects.filter(is_active=True).select_related('listing')
        active = [b for b in qs if b.listing is None or b.listing.is_active]
        return {
            'active_banners': active,
            'banner_rotation_seconds': settings.banner_rotation_seconds,
        }
    except Exception:
        return {'active_banners': [], 'banner_rotation_seconds': 5}
