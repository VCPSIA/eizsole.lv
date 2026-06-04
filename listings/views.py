from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q, Count
from django.core.cache import cache
from .models import Category, Listing, ListingImage, ListingVideo, Report, Equipment, Message, AutoDetails, TireDetails, RealEstateDetails, SiteSettings, VinReport, DiscountCode, Favorite, Banner, SavedSearch, ListingView
from .profanity import contains_profanity
from .ai_moderation import check_listing_images
from .contact_filter import contains_contact_info
from auctions.models import Auction
import datetime
from datetime import timedelta

DURATION_CHOICES = [
    ('7',  '1 nedēļa'),
    ('14', '2 nedēļas'),
    ('21', '3 nedēļas'),
    ('28', '4 nedēļas'),
]


def is_admin(user):
    return user.is_authenticated and user.is_staff


def _validate_price(value_str, field_name='Cena'):
    """Atgriež (Decimal, None) vai (None, kļūdas ziņojums). Tukša virkne → (None, None) — obligātumu pārbauda izsaucējs."""
    from decimal import Decimal, InvalidOperation
    s = (value_str or '').strip()
    if not s:
        return None, None
    if 'e' in s.lower():
        return None, f'{field_name} — zinātniskais pieraksts nav atļauts.'
    try:
        val = Decimal(s)
    except InvalidOperation:
        return None, f'{field_name} — nederīgs skaitlis.'
    if val <= 0:
        return None, f'{field_name} jābūt pozitīvam skaitlim.'
    if val > Decimal('9999999'):
        return None, f'{field_name} nevar pārsniegt €9 999 999.'
    return val, None


AUTO_DETAIL_SLUGS = set()
YEAR_REQUIRED_SLUGS = set()
TIRE_SLUGS = set()
TIRE_EXCLUDE_SLUGS = set()
RE_SLUGS = set()
DATING_SLUGS = {'iepazisanas'}


def _is_auto_category(category):
    c = category
    while c:
        if c.slug in AUTO_DETAIL_SLUGS:
            return True
        c = c.parent
    return False


def _is_year_required_category(category):
    c = category
    while c:
        if c.slug in YEAR_REQUIRED_SLUGS:
            return True
        c = c.parent
    return False


def _is_tire_category(category):
    c = category
    while c:
        if c.slug in TIRE_EXCLUDE_SLUGS:
            return False
        if c.slug in TIRE_SLUGS:
            return True
        c = c.parent
    return False


def _save_tire_details(listing, post):
    TireDetails.objects.update_or_create(
        listing=listing,
        defaults=dict(
            radius=post.get('tire_radius') or 0,
            width=post.get('tire_width') or 0,
            profile=post.get('tire_profile') or 0,
            season=post.get('tire_season', ''),
            manufacturer=post.get('tire_manufacturer', '').strip(),
            load_index=post.get('tire_load_index') or None,
            speed_index=post.get('tire_speed_index', '').strip().upper(),
        )
    )


def _is_re_category(category):
    c = category
    while c:
        if c.slug in RE_SLUGS:
            return True
        c = c.parent
    return False


def _is_dating_category(category):
    c = category
    while c:
        if c.slug in DATING_SLUGS:
            return True
        c = c.parent
    return False


WORK_SERVICE_IDS = {10, 11, 935}  # Darbs, Pakalpojumi, Iepazīties

def _is_work_service_category(category):
    c = category
    while c:
        if c.id in WORK_SERVICE_IDS:
            return True
        c = c.parent
    return False


def _save_re_details(listing, post):
    RealEstateDetails.objects.update_or_create(
        listing=listing,
        defaults=dict(
            deal_type=post.get('re_deal_type', ''),
            country=post.get('re_country', '').strip(),
            district=post.get('re_district', '').strip(),
            city=post.get('re_city', '').strip(),
        )
    )


def _save_auto_details(listing, post):
    has_inspection = bool(post.get('has_inspection'))
    inspection_date = post.get('inspection_date') or None
    AutoDetails.objects.update_or_create(
        listing=listing,
        defaults=dict(
            engine_type=post.get('engine_type', ''),
            engine_volume=post.get('engine_volume', 0),
            transmission=post.get('transmission', ''),
            body_type=post.get('body_type', ''),
            mileage=int(post.get('mileage', 0) or 0),
            has_inspection=has_inspection,
            inspection_date=inspection_date if has_inspection else None,
            reg_number=post.get('reg_number', '').strip().upper(),
            vin=post.get('vin', '').strip().upper(),
        )
    )


CITY_SLUGS = {
    'riga':        'Rīga',
    'daugavpils':  'Daugavpils',
    'liepaja':     'Liepāja',
    'jelgava':     'Jelgava',
    'jurmala':     'Jūrmala',
    'ventspils':   'Ventspils',
    'rezekne':     'Rēzekne',
    'valmiera':    'Valmiera',
    'jekabpils':   'Jēkabpils',
    'ogre':        'Ogre',
    'cesis':       'Cēsis',
    'salaspils':   'Salaspils',
    'tukums':      'Tukums',
    'sigulda':     'Sigulda',
    'bauska':      'Bauska',
}


def _active_listings():
    return Listing.objects.filter(
        is_active=True,
        moderation_status='approved',
    ).filter(Q(expires_at__isnull=True) | Q(expires_at__gt=timezone.now()))


def city_listings(request, city_slug):
    from django.http import Http404
    city_name = CITY_SLUGS.get(city_slug)
    if not city_name:
        raise Http404
    listings = list(
        _active_listings()
        .filter(Q(city__icontains=city_name) | Q(location__icontains=city_name),
                is_auction=False)
        .order_by('-is_featured', '-featured_at', '-created_at')
        .prefetch_related('images')[:48]
    )
    return render(request, 'listings/city.html', {
        'city_name':  city_name,
        'city_slug':  city_slug,
        'listings':   listings,
        'all_cities': CITY_SLUGS,
    })


def home(request):
    # Kategorijas — kešo 1 stundu (mainās reti)
    categories = cache.get('home_categories')
    if categories is None:
        categories = list(Category.objects.filter(parent=None))
        cache.set('home_categories', categories, 3600)

    deal_type_filter = request.GET.get('deal_type', '')

    # Sludinājumi — kešo 5 min, atsevišķi katram deal_type filtram
    listings_key = f'home_listings_{deal_type_filter or "all"}'
    latest_listings = cache.get(listings_key)
    if latest_listings is None:
        qs = _active_listings().filter(is_auction=False)
        if deal_type_filter == 'offer':
            iepazities_ids = list(Category.objects.filter(
                Q(id=935) | Q(parent=935) | Q(parent__parent=935)
            ).values_list('id', flat=True))
            qs = qs.filter(Q(deal_type='offer') | Q(category_id__in=iepazities_ids))
        elif deal_type_filter:
            qs = qs.filter(deal_type=deal_type_filter)
        latest_listings = list(
            qs.order_by('-is_featured', '-featured_at', '-created_at')
            .prefetch_related('images')[:12]
        )
        cache.set(listings_key, latest_listings, 300)

    # Izsoles — kešo 2 min
    active_auctions = cache.get('home_active_auctions')
    if active_auctions is None:
        active_auctions = list(
            Auction.objects.filter(is_finished=False)
            .select_related('listing')
            .prefetch_related('listing__images')
            .order_by('-listing__is_featured', '-listing__featured_at', 'ends_at')[:6]
        )
        cache.set('home_active_auctions', active_auctions, 120)

    # Pēdējās skatītās — sesijas specifiskas, nekešo
    recently_ids = request.session.get('recently_viewed', [])
    recently_viewed = list(Listing.objects.filter(pk__in=recently_ids, is_active=True).prefetch_related('images'))
    recently_viewed.sort(key=lambda l: recently_ids.index(l.pk) if l.pk in recently_ids else 999)

    return render(request, 'listings/home.html', {
        'categories': categories,
        'latest_listings': latest_listings,
        'active_auctions': active_auctions,
        'recently_viewed': recently_viewed,
        'active_deal_type': deal_type_filter,
        'deal_type_choices': Listing.DEAL_TYPE_CHOICES,
    })


def category(request, slug):
    cat = get_object_or_404(Category, slug=slug)
    subcategories = cat.children.all()

    def collect_all(c):
        result = [c]
        for child in c.children.all():
            result.extend(collect_all(child))
        return result

    all_cats = collect_all(cat)
    listings = _active_listings().filter(category__in=all_cats).order_by('-is_featured', '-featured_at', '-created_at')

    top_parent = cat
    while top_parent.parent:
        top_parent = top_parent.parent

    active_slugs = []
    c = cat
    while c:
        active_slugs.append(c.slug)
        c = c.parent

    show_auto_filters = _is_auto_category(cat)
    show_tire_filters = _is_tire_category(cat) or cat.slug in TIRE_SLUGS
    show_dating_filters = _is_dating_category(cat)
    f = request.GET

    if show_auto_filters:
        if f.get('price_min'):
            listings = listings.filter(price__gte=f['price_min'])
        if f.get('price_max'):
            listings = listings.filter(price__lte=f['price_max'])
        if f.get('year_min'):
            listings = listings.filter(year__gte=f['year_min'])
        if f.get('year_max'):
            listings = listings.filter(year__lte=f['year_max'])
        if f.get('engine_type'):
            listings = listings.filter(auto_details__engine_type=f['engine_type'])
        if f.get('transmission'):
            listings = listings.filter(auto_details__transmission=f['transmission'])
        if f.get('body_type'):
            listings = listings.filter(auto_details__body_type=f['body_type'])
        if f.get('volume_min'):
            listings = listings.filter(auto_details__engine_volume__gte=f['volume_min'])
        if f.get('volume_max'):
            listings = listings.filter(auto_details__engine_volume__lte=f['volume_max'])
        if f.get('mileage_max'):
            listings = listings.filter(auto_details__mileage__lte=f['mileage_max'])
        if f.get('deal_type'):
            listings = listings.filter(deal_type=f['deal_type'])

    if show_tire_filters:
        if f.get('price_min'):
            listings = listings.filter(price__gte=f['price_min'])
        if f.get('price_max'):
            listings = listings.filter(price__lte=f['price_max'])
        if f.get('condition'):
            listings = listings.filter(condition=f['condition'])
        if f.get('manufacturer'):
            listings = listings.filter(tire_details__manufacturer__icontains=f['manufacturer'])
        if f.get('season'):
            listings = listings.filter(tire_details__season=f['season'])
        if f.get('width'):
            listings = listings.filter(tire_details__width=f['width'])
        if f.get('profile'):
            listings = listings.filter(tire_details__profile=f['profile'])
        if f.get('radius'):
            listings = listings.filter(tire_details__radius=f['radius'])
        if f.get('load_min'):
            listings = listings.filter(tire_details__load_index__gte=f['load_min'])
        if f.get('load_max'):
            listings = listings.filter(tire_details__load_index__lte=f['load_max'])
        if f.get('speed_index'):
            listings = listings.filter(tire_details__speed_index__iexact=f['speed_index'])

    if show_dating_filters:
        if f.get('age_range'):
            listings = listings.filter(age_range=f['age_range'])
        if f.get('city'):
            listings = listings.filter(city__icontains=f['city'])
        if f.get('subcat'):
            try:
                subcat = Category.objects.get(pk=f['subcat'])
                def collect_all(c):
                    r = [c]
                    for ch in c.children.all():
                        r.extend(collect_all(ch))
                    return r
                listings = listings.filter(category__in=collect_all(subcat))
            except Category.DoesNotExist:
                pass

    if not show_auto_filters and not show_tire_filters and not show_dating_filters:
        if f.get('price_min'):
            listings = listings.filter(price__gte=f['price_min'])
        if f.get('price_max'):
            listings = listings.filter(price__lte=f['price_max'])
        if f.get('condition'):
            listings = listings.filter(condition=f['condition'])
        if f.get('deal_type'):
            listings = listings.filter(deal_type=f['deal_type'])
        if f.get('country'):
            listings = listings.filter(country__icontains=f['country'])
        if f.get('listing_type') == 'auction':
            listings = listings.filter(is_auction=True)
        elif f.get('listing_type') == 'listing':
            listings = listings.filter(is_auction=False)

    per_page_options = [10, 25, 50, 100]
    try:
        per_page = int(f.get('per_page', 25))
        if per_page not in per_page_options:
            per_page = 25
    except (ValueError, TypeError):
        per_page = 25

    from django.core.paginator import Paginator
    paginator = Paginator(listings, per_page)
    try:
        page_obj = paginator.get_page(f.get('page', 1))
    except Exception:
        page_obj = paginator.get_page(1)

    return render(request, 'listings/category.html', {
        'category': cat,
        'subcategories': subcategories,
        'top_parent': top_parent,
        'active_slugs': active_slugs,
        'listings': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
        'per_page': per_page,
        'per_page_options': per_page_options,
        'show_auto_filters': show_auto_filters,
        'show_tire_filters': show_tire_filters,
        'show_dating_filters': show_dating_filters,
        'dating_subcats': cat.children.all() if show_dating_filters and cat.slug == 'iepazisanas' else [],
        'age_range_choices': [('18-30','18–30 gadi'),('30-45','30–45 gadi'),('45-60','45–60 gadi'),('60+','No 60 gadiem')],
        'auto_choices': {
            'engine_types': AutoDetails.ENGINE_CHOICES,
            'transmissions': AutoDetails.TRANSMISSION_CHOICES,
            'body_types': AutoDetails.BODY_CHOICES,
        },
        'tire_season_choices': TireDetails.SEASON_CHOICES,
        'condition_choices': [('new','Jauns'),('used','Lietots'),('damaged','Bojāts')],
        'f': f,
        'compare_ids': request.session.get('compare_ids', []),
        'fav_ids': list(Favorite.objects.filter(user=request.user).values_list('listing_id', flat=True)) if request.user.is_authenticated else [],
    })


def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    # Rāda tikai aktīvus, izņemot pašam sludinājuma autoram un adminiem
    if not listing.is_active and not (request.user == listing.seller or (request.user.is_authenticated and request.user.is_staff)):
        from django.http import Http404
        raise Http404
    if listing.is_active:
        Listing.objects.filter(pk=pk).update(views=listing.views + 1)
        source = ListingView.detect_source(request.META.get('HTTP_REFERER', ''))
        ListingView.objects.create(listing=listing, source=source)
    # Saglabā pēdējās skatītās sesijā
    recently = request.session.get('recently_viewed', [])
    if pk in recently:
        recently.remove(pk)
    recently.insert(0, pk)
    request.session['recently_viewed'] = recently[:8]

    auction = getattr(listing, 'auction', None)
    is_favorited = request.user.is_authenticated and Favorite.objects.filter(user=request.user, listing=listing).exists()
    related = (_active_listings()
               .filter(category=listing.category)
               .exclude(pk=listing.pk)
               .order_by('-created_at')[:4])

    # Iekšējās saites — pilsētas slug
    city_slug = None
    if listing.city:
        city_lower = listing.city.lower()
        for slug, name in CITY_SLUGS.items():
            if name.lower() == city_lower or slug in city_lower:
                city_slug = slug
                break

    # Saistīts blog raksts
    from blog.models import BlogPost
    cat_name = listing.category.name.lower()
    blog_post = BlogPost.objects.filter(
        is_published=True,
        meta_keywords__icontains=cat_name
    ).first() or BlogPost.objects.filter(is_published=True).first()

    return render(request, 'listings/detail.html', {
        'listing':      listing,
        'auction':      auction,
        'site_settings': SiteSettings.get(),
        'is_favorited': is_favorited,
        'related':      related,
        'is_dating':    _is_dating_category(listing.category),
        'city_slug':    city_slug,
        'blog_post':    blog_post,
        'all_cities':   CITY_SLUGS,
    })


def search(request):
    query    = request.GET.get('q', '')
    f        = request.GET
    listings = _active_listings()
    if query:
        listings = listings.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if f.get('price_min'):
        listings = listings.filter(price__gte=f['price_min'])
    if f.get('price_max'):
        listings = listings.filter(price__lte=f['price_max'])
    if f.get('condition'):
        listings = listings.filter(condition=f['condition'])
    if f.get('category'):
        try:
            cat = Category.objects.get(pk=f['category'])
            def collect_all(c):
                r = [c]
                for ch in c.children.all(): r.extend(collect_all(ch))
                return r
            listings = listings.filter(category__in=collect_all(cat))
        except Category.DoesNotExist:
            pass
    if f.get('listing_type') == 'auction':
        listings = listings.filter(is_auction=True)
    elif f.get('listing_type') == 'listing':
        listings = listings.filter(is_auction=False)
    listings = listings.order_by('-is_featured', '-featured_at', '-created_at')
    top_categories = Category.objects.filter(parent=None).order_by('order', 'pk')
    return render(request, 'listings/search.html', {
        'listings': listings,
        'query': query,
        'f': f,
        'top_categories': top_categories,
        'condition_choices': [('new','Jauns'),('used','Lietots'),('damaged','Bojāts')],
    })


def subcategories_json(request, pk):
    children = Category.objects.filter(parent_id=pk).values('id', 'name', 'slug')
    return JsonResponse({'subcategories': list(children)})


@login_required
def listing_create(request):
    categories = Category.objects.filter(parent=None)
    current_year = datetime.date.today().year
    years = list(range(current_year, 1899, -1))
    equipment_by_group = {}
    for eq in Equipment.objects.all():
        equipment_by_group.setdefault(eq.get_group_display(), []).append(eq)
    auto_detail_ids = list(
        Category.objects.filter(slug__in=AUTO_DETAIL_SLUGS).values_list('id', flat=True)
    )
    tire_detail_ids = list(
        Category.objects.filter(slug__in=TIRE_SLUGS).values_list('id', flat=True)
    )
    tire_exclude_ids = list(
        Category.objects.filter(slug__in=TIRE_EXCLUDE_SLUGS).values_list('id', flat=True)
    )
    re_cat_ids = list(
        Category.objects.filter(slug__in=RE_SLUGS).values_list('id', flat=True)
    )
    year_required_ids = list(
        Category.objects.filter(slug__in=YEAR_REQUIRED_SLUGS).values_list('id', flat=True)
    )

    def ctx(extra=None):
        base = {'categories': categories, 'years': years,
                'equipment_by_group': equipment_by_group,
                'duration_choices': DURATION_CHOICES,
                'auto_detail_ids': auto_detail_ids,
                'tire_detail_ids': tire_detail_ids,
                'tire_exclude_ids': tire_exclude_ids,
                're_cat_ids': re_cat_ids,
                'year_required_ids': year_required_ids,
                'auto_choices': {
                    'engine_types': AutoDetails.ENGINE_CHOICES,
                    'transmissions': AutoDetails.TRANSMISSION_CHOICES,
                    'body_types': AutoDetails.BODY_CHOICES,
                },
                'tire_season_choices': TireDetails.SEASON_CHOICES,
                're_deal_choices': RealEstateDetails.DEAL_CHOICES,
                'deal_type_choices': Listing.DEAL_TYPE_CHOICES,
                'site_settings': SiteSettings.get(),
                'user_accepted_cent_rules': (
                    __import__('auctions.models', fromlist=['CentAuctionRulesAcceptance'])
                    .CentAuctionRulesAcceptance.objects.filter(user=request.user).exists()
                    if request.user.is_authenticated else False
                ),
                'profile_country': request.user.profile.country if hasattr(request.user, 'profile') else '',
                'profile_city': request.user.profile.city if hasattr(request.user, 'profile') else '',
                'google_maps_api_key': getattr(__import__('django.conf', fromlist=['settings']).settings, 'GOOGLE_MAPS_API_KEY', ''),
                }
        if extra:
            base.update(extra)
        return base

    if request.method == 'POST':
        # Rate limiting: max 5 sludinājumi stundā vienam lietotājam
        recent = Listing.objects.filter(
            seller=request.user,
            created_at__gte=timezone.now() - timedelta(hours=1),
        ).count()
        if recent >= 5:
            messages.error(request, 'Esat sasniedzis publicēšanas limitu — maksimum 5 sludinājumi stundā. Lūdzu mēģiniet vēlāk.')
            return render(request, 'listings/create.html', ctx())

        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()

        if len(title) < 3:
            messages.error(request, 'Nosaukums ir pārāk īss — minimums 3 rakstzīmes.')
            return render(request, 'listings/create.html', ctx({'post': request.POST}))
        if len(title) > 200:
            messages.error(request, 'Nosaukums ir pārāk garš — maksimums 200 rakstzīmes.')
            return render(request, 'listings/create.html', ctx({'post': request.POST}))
        if len(description) > 10000:
            messages.error(request, 'Apraksts ir pārāk garš — maksimums 10 000 rakstzīmes.')
            return render(request, 'listings/create.html', ctx({'post': request.POST}))

        _deal_type_pre = request.POST.get('deal_type', '')
        _is_auction_pre = 'is_auction' in request.POST
        if not _is_auction_pre and _deal_type_pre != 'give':
            _, price_err = _validate_price(request.POST.get('price', ''))
            if price_err:
                messages.error(request, price_err)
                return render(request, 'listings/create.html', ctx({'post': request.POST}))

        if contains_profanity(title) or contains_profanity(description):
            messages.error(request, 'Sludinājumā konstatēts nepiemērots saturs. Lūdzu pārbaudiet tekstu un mēģiniet vēlreiz.')
            return render(request, 'listings/create.html', ctx({'post': request.POST}))

        # Auto obligātie lauki
        cat_pk = request.POST.get('category')
        if cat_pk:
            try:
                cat_obj = Category.objects.get(pk=cat_pk)
                if _is_auto_category(cat_obj):
                    auto_required = ['engine_type', 'engine_volume', 'transmission', 'body_type', 'mileage', 'reg_number', 'vin', 'year']
                    missing = [f for f in auto_required if not request.POST.get(f, '').strip()]
                    if missing:
                        messages.error(request, 'Lūdzu aizpildiet visus obligātos auto lauksus (ieskaitot izgatavošanas gadu).')
                        return render(request, 'listings/create.html', ctx({'post': request.POST}))
                if _is_tire_category(cat_obj):
                    tire_required = ['tire_radius', 'tire_width', 'tire_profile', 'tire_season', 'tire_manufacturer']
                    missing = [f for f in tire_required if not request.POST.get(f, '').strip()]
                    if missing:
                        messages.error(request, 'Lūdzu aizpildiet visus obligātos riepas lauksus.')
                        return render(request, 'listings/create.html', ctx({'post': request.POST}))
                if _is_re_category(cat_obj):
                    re_required = ['re_deal_type', 're_country', 're_district', 're_city']
                    missing = [f for f in re_required if not request.POST.get(f, '').strip()]
                    if missing:
                        messages.error(request, 'Lūdzu aizpildiet visus obligātos nekustamā īpašuma lauksus.')
                        return render(request, 'listings/create.html', ctx({'post': request.POST}))
                if _is_year_required_category(cat_obj):
                    if not request.POST.get('year', '').strip():
                        messages.error(request, 'Lūdzu norādiet izgatavošanas gadu.')
                        return render(request, 'listings/create.html', ctx({'post': request.POST}))
            except Category.DoesNotExist:
                pass

        # Kontaktinformācija obligāta
        contact_phone = request.POST.get('contact_phone', '').strip()
        contact_email = request.POST.get('contact_email', '').strip()
        if not contact_phone:
            messages.error(request, 'Tālruņa numurs ir obligāts.')
            return render(request, 'listings/create.html', ctx({'post': request.POST}))
        if not contact_email:
            messages.error(request, 'E-pasta adrese ir obligāta.')
            return render(request, 'listings/create.html', ctx({'post': request.POST}))

        # Vismaz viena bilde obligāta (izņemot iepazīšanās)
        is_dating = cat_pk and _is_dating_category(get_object_or_404(Category, pk=cat_pk))
        uploaded_images = request.FILES.getlist('images')
        if not uploaded_images and not is_dating:
            messages.error(request, 'Lūdzu pievienojiet vismaz vienu fotogrāfiju.')
            return render(request, 'listings/create.html', ctx({'post': request.POST}))

        # Bilžu servera validācija
        _ALLOWED_IMG = {'image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/heic', 'image/heif'}
        _MAX_IMG_SIZE = 10 * 1024 * 1024  # 10 MB
        if len(uploaded_images) > 8:
            messages.error(request, 'Maksimums 8 bildes atļautas.')
            return render(request, 'listings/create.html', ctx({'post': request.POST}))
        for _img in uploaded_images:
            if _img.content_type not in _ALLOWED_IMG:
                messages.error(request, f'Atbalstīti tikai JPG, PNG, WEBP formāti ({_img.name}).')
                return render(request, 'listings/create.html', ctx({'post': request.POST}))
            if _img.size > _MAX_IMG_SIZE:
                messages.error(request, f'Bilde pārāk liela — maks. 10 MB ({_img.name}).')
                return render(request, 'listings/create.html', ctx({'post': request.POST}))

        is_auction = 'is_auction' in request.POST

        if is_auction and request.POST.get('deal_type', '') == 'give':
            messages.error(request, '"Atdod" nevar pievienot izsolei.')
            return render(request, 'listings/create.html', ctx({'post': request.POST}))

        if request.POST.get('deal_type', '') == 'offer':
            _cat_check = Category.objects.filter(pk=request.POST.get('category', 0)).first()
            if not _cat_check or not _is_work_service_category(_cat_check):
                messages.error(request, '"Piedāvā" ir pieejams tikai Darba un Pakalpojumu sludinājumiem.')
                return render(request, 'listings/create.html', ctx({'post': request.POST}))

        # Atlaižu kods
        promo_code_str = request.POST.get('promo_code', '').strip().upper()
        promo_obj = None
        promo_saved = None
        if promo_code_str:
            try:
                promo_obj = DiscountCode.objects.get(code__iexact=promo_code_str)
                valid, err = promo_obj.is_valid()
                if not valid:
                    messages.error(request, f'Atlaižu kods: {err}')
                    return render(request, 'listings/create.html', ctx({'post': request.POST}))
            except DiscountCode.DoesNotExist:
                messages.error(request, 'Atlaižu kods nav atrasts.')
                return render(request, 'listings/create.html', ctx({'post': request.POST}))

        # Maksu pārbaude
        settings = SiteSettings.get()
        from accounts.models import Wallet, WalletTransaction
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        if is_auction and settings.auction_fee_enabled and settings.auction_fee > 0:
            base_fee = settings.auction_fee
        elif not is_auction and settings.listing_fee_enabled and settings.listing_fee > 0:
            base_fee = settings.listing_fee
        else:
            base_fee = None

        if base_fee:
            if promo_obj:
                fee, promo_saved = promo_obj.apply(base_fee)
            else:
                fee = base_fee
            if wallet.balance < fee:
                orig = f' (sākotnēji €{base_fee})' if promo_saved else ''
                messages.error(request, f'Nepietiek līdzekļu makā. Maksa ir €{fee}{orig}. Jūsu atlikums: €{wallet.balance}.')
                return render(request, 'listings/create.html', ctx({'post': request.POST}))
        else:
            fee = None

        # TOP maksu pārbaude
        want_featured = 'want_featured' in request.POST
        if want_featured:
            if is_auction and settings.featured_auction_enabled and settings.featured_auction_fee > 0:
                featured_fee = settings.featured_auction_fee
            elif not is_auction and settings.featured_listing_enabled and settings.featured_listing_fee > 0:
                featured_fee = settings.featured_listing_fee
            else:
                featured_fee = None
                want_featured = False
            if featured_fee and wallet.balance < (fee or 0) + featured_fee:
                messages.error(request, f'Nepietiek līdzekļu TOP vietai. TOP maksa ir €{featured_fee}. Jūsu atlikums: €{wallet.balance}.')
                return render(request, 'listings/create.html', ctx({'post': request.POST}))
        else:
            featured_fee = None

        # Banera maksu pārbaude
        want_banner = 'want_banner' in request.POST and bool(request.FILES.get('banner_image'))
        if want_banner and settings.banner_enabled and settings.banner_fee > 0:
            banner_fee = settings.banner_fee
            total_so_far = (fee or 0) + (featured_fee or 0)
            if wallet.balance < total_so_far + banner_fee:
                messages.error(request, f'Nepietiek līdzekļu banerim. Banera maksa ir €{banner_fee}. Jūsu atlikums: €{wallet.balance}.')
                return render(request, 'listings/create.html', ctx({'post': request.POST}))
        else:
            banner_fee = None
            want_banner = False

        if is_auction:
            expires_at = None
            sp_val, sp_err = _validate_price(request.POST.get('starting_price', ''), 'Sākumcena')
            if sp_err:
                messages.error(request, sp_err)
                return render(request, 'listings/create.html', ctx({'post': request.POST}))
            if sp_val is None:
                messages.error(request, 'Sākumcena ir obligāta.')
                return render(request, 'listings/create.html', ctx({'post': request.POST}))
            _, bn_err = _validate_price(request.POST.get('buy_now_price', ''), 'Pērc tūlīt cena')
            if bn_err:
                messages.error(request, bn_err)
                return render(request, 'listings/create.html', ctx({'post': request.POST}))
            _, rp_err = _validate_price(request.POST.get('reserve_price', ''), 'Rezerves cena')
            if rp_err:
                messages.error(request, rp_err)
                return render(request, 'listings/create.html', ctx({'post': request.POST}))
        else:
            duration_days = int(request.POST.get('duration', 7))
            if duration_days not in [7, 14, 21, 28]:
                duration_days = 7
            expires_at = timezone.now() + timedelta(days=duration_days)

        year_val = request.POST.get('year') or None
        cat_for_listing = get_object_or_404(Category, pk=request.POST['category'])
        listing = Listing.objects.create(
            title=title,
            description=description,
            category=cat_for_listing,
            seller=request.user,
            price=None if request.POST.get('deal_type') == 'give' else (request.POST.get('price') or None),
            condition=request.POST.get('condition', 'used'),
            deal_type=request.POST.get('deal_type', '') if not is_auction else '',
            year=year_val,
            location=request.POST.get('location', ''),
            country=request.POST.get('country', '').strip(),
            city=request.POST.get('city', '').strip(),
            is_auction=is_auction,
            expires_at=expires_at,
            contact_email=contact_email,
            contact_phone=contact_phone,
            age_range=request.POST.get('age_range', '') if _is_dating_category(cat_for_listing) else '',
            gender=request.POST.get('gender', '') if _is_dating_category(cat_for_listing) else '',
            seeking=request.POST.get('seeking', '') if _is_dating_category(cat_for_listing) else '',
        )
        equipment_ids = request.POST.getlist('equipment')
        if equipment_ids:
            listing.equipment.set(Equipment.objects.filter(pk__in=equipment_ids))

        # Auto / riepas / NĪ detaļas
        if _is_auto_category(cat_for_listing):
            _save_auto_details(listing, request.POST)
        elif _is_tire_category(cat_for_listing):
            _save_tire_details(listing, request.POST)
        elif _is_re_category(cat_for_listing):
            _save_re_details(listing, request.POST)

        # Bildes — jau validētas augstāk
        for i, img in enumerate(uploaded_images):
            ListingImage.objects.create(listing=listing, image=img, order=i)

        # AI bilžu moderācija
        mod_result = check_listing_images(listing)
        if not mod_result['safe']:
            listing.moderation_status = 'pending'
            listing.is_active = False
            if mod_result['flags']:
                reasons = '; '.join(f['reason'] for f in mod_result['flags'] if f.get('reason'))
                listing.moderation_note = f'AI karodziņš: {reasons}'
            listing.save()
            messages.warning(request, 'Jūsu sludinājums gaida moderatora apstiprināšanu. Mēs to izskatīsim pēc iespējas ātrāk.')
            return redirect('listing_detail', pk=listing.pk)

        # Video — max 1
        video_file = request.FILES.get('video')
        if video_file:
            allowed = ['video/mp4', 'video/webm', 'video/quicktime', 'video/avi', 'video/x-matroska']
            if video_file.content_type in allowed or video_file.name.lower().endswith(('.mp4', '.webm', '.mov', '.avi', '.mkv')):
                ListingVideo.objects.create(listing=listing, file=video_file)

        if listing.is_auction:
            ends_at_raw = request.POST.get('ends_at', '')
            try:
                from django.utils.dateparse import parse_datetime
                ends_at_dt = parse_datetime(ends_at_raw)
                if ends_at_dt is None:
                    raise ValueError
                import pytz
                if timezone.is_naive(ends_at_dt):
                    ends_at_dt = timezone.make_aware(ends_at_dt)
                max_ends = timezone.now() + timedelta(days=30)
                min_ends = timezone.now() + timedelta(hours=1)
                if ends_at_dt > max_ends:
                    ends_at_dt = max_ends
                if ends_at_dt < min_ends:
                    ends_at_dt = min_ends
            except (ValueError, Exception):
                ends_at_dt = timezone.now() + timedelta(days=7)
            auction_type = request.POST.get('auction_type', 'english')
            is_cent = 'is_cent_auction' in request.POST

            # Centu izsoles noteikumu piekrišana no formas
            if is_cent and 'cent_rules_agree' in request.POST:
                from auctions.models import CentAuctionRulesAcceptance
                ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))[:45]
                CentAuctionRulesAcceptance.objects.get_or_create(
                    user=request.user,
                    defaults={'ip_address': ip}
                )
            dutch_step, _ = _validate_price(request.POST.get('dutch_price_step', ''))
            dutch_min, _  = _validate_price(request.POST.get('dutch_min_price', ''))
            try:
                dutch_interval = int(request.POST.get('dutch_interval_minutes', 60))
                if dutch_interval < 1:
                    dutch_interval = 60
            except (ValueError, TypeError):
                dutch_interval = 60
            Auction.objects.create(
                listing=listing,
                auction_type=auction_type,
                is_cent_auction=is_cent,
                delivery_method=request.POST.get('delivery_method', '') if is_cent else '',
                starting_price=sp_val,
                current_price=sp_val,
                min_bid_increment=request.POST.get('min_bid_increment', 1),
                ends_at=ends_at_dt,
                buy_now_price=_validate_price(request.POST.get('buy_now_price', ''))[0] if auction_type == 'english' else None,
                reserve_price=_validate_price(request.POST.get('reserve_price', ''))[0] if auction_type == 'english' else None,
                dutch_price_step=dutch_step if auction_type == 'dutch' else None,
                dutch_interval_minutes=dutch_interval if auction_type == 'dutch' else None,
                dutch_min_price=dutch_min if auction_type == 'dutch' else None,
            )

        # Novilkt maksu no maka
        if fee:
            desc = 'Izsoles publicēšanas maksa' if is_auction else 'Sludinājuma publicēšanas maksa'
            if promo_saved:
                desc += f' (atlaide €{promo_saved}, kods: {promo_obj.code})'
            WalletTransaction.make_spend(wallet, fee, description=desc, reference=f'LIST-{listing.pk}')
            if promo_obj:
                DiscountCode.objects.filter(pk=promo_obj.pk).update(used_count=promo_obj.used_count + 1)

        # TOP sludinājums
        if want_featured and featured_fee:
            Listing.objects.filter(is_auction=is_auction, is_featured=True).update(is_featured=False, featured_at=None)
            listing.is_featured = True
            listing.featured_at = timezone.now()
            listing.save(update_fields=['is_featured', 'featured_at'])
            desc = 'TOP izsole' if is_auction else 'TOP sludinājums'
            WalletTransaction.make_spend(wallet, featured_fee, description=desc, reference=f'TOP-{listing.pk}')

        # Baneris
        if want_banner and banner_fee:
            Banner.objects.create(
                listing=listing,
                user=request.user,
                image=request.FILES['banner_image'],
                link_url=request.POST.get('banner_link_url', '').strip(),
            )
            WalletTransaction.make_spend(wallet, banner_fee, description='Reklāmas baneris', reference=f'BAN-{listing.pk}')

        if is_auction:
            messages.success(request, 'Izsole veiksmīgi publicēta!')
        else:
            messages.success(request, 'Sludinājums veiksmīgi publicēts!')
        return redirect('listing_detail', pk=listing.pk)
    try:
        profile = request.user.profile
        profile_country = profile.country
        profile_city = profile.city
    except Exception:
        profile_country = ''
        profile_city = ''
    return render(request, 'listings/create.html', ctx({'profile_country': profile_country, 'profile_city': profile_city}))


@login_required
def banner_create(request):
    settings = SiteSettings.get()
    if not settings.banner_enabled:
        messages.error(request, 'Baneru publicēšana pašlaik nav pieejama.')
        return redirect('home')

    if request.method == 'POST':
        image = request.FILES.get('banner_image')
        if not image:
            messages.error(request, 'Lūdzu augšupielādējiet banera attēlu.')
            return render(request, 'listings/banner_create.html', {'site_settings': settings})
        if image.content_type not in _ALLOWED_IMG:
            messages.error(request, 'Banerim atbalstīti tikai JPG, PNG, WEBP formāti.')
            return render(request, 'listings/banner_create.html', {'site_settings': settings})
        if image.size > _MAX_IMG_SIZE:
            messages.error(request, 'Banera bilde pārāk liela — maks. 10 MB.')
            return render(request, 'listings/banner_create.html', {'site_settings': settings})

        from accounts.models import Wallet, WalletTransaction
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        fee = settings.banner_fee if settings.banner_fee > 0 else None
        if fee and wallet.balance < fee:
            messages.error(request, f'Nepietiek līdzekļu. Banera maksa: €{fee}. Jūsu atlikums: €{wallet.balance}.')
            return render(request, 'listings/banner_create.html', {'site_settings': settings})

        Banner.objects.create(
            user=request.user,
            image=image,
            text=request.POST.get('banner_text', '').strip(),
            link_url=request.POST.get('banner_link_url', '').strip(),
        )
        if fee:
            WalletTransaction.make_spend(wallet, fee, description='Reklāmas baneris', reference='BAN-standalone')
        messages.success(request, 'Baneris veiksmīgi publicēts!')
        return redirect('profile')

    return render(request, 'listings/banner_create.html', {'site_settings': settings})


@login_required
def listing_edit(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user, is_auction=False)
    categories = Category.objects.filter(parent=None)
    current_year = datetime.date.today().year
    years = list(range(current_year, 1899, -1))
    equipment_by_group = {}
    for eq in Equipment.objects.all():
        equipment_by_group.setdefault(eq.get_group_display(), []).append(eq)
    is_auto = _is_auto_category(listing.category)
    auto_detail_ids = list(
        Category.objects.filter(slug__in=AUTO_DETAIL_SLUGS).values_list('id', flat=True)
    )
    tire_detail_ids = list(
        Category.objects.filter(slug__in=TIRE_SLUGS).values_list('id', flat=True)
    )
    tire_exclude_ids = list(
        Category.objects.filter(slug__in=TIRE_EXCLUDE_SLUGS).values_list('id', flat=True)
    )
    is_tire = _is_tire_category(listing.category)
    is_re = _is_re_category(listing.category)
    is_year_required = _is_year_required_category(listing.category)
    re_cat_ids = list(
        Category.objects.filter(slug__in=RE_SLUGS).values_list('id', flat=True)
    )
    year_required_ids = list(
        Category.objects.filter(slug__in=YEAR_REQUIRED_SLUGS).values_list('id', flat=True)
    )

    def ctx(extra=None):
        base = {
            'listing': listing,
            'categories': categories,
            'years': years,
            'equipment_by_group': equipment_by_group,
            'is_auto': is_auto,
            'is_tire': is_tire,
            'is_re': is_re,
            'is_year_required': is_year_required,
            'auto_detail_ids': auto_detail_ids,
            'tire_detail_ids': tire_detail_ids,
            'tire_exclude_ids': tire_exclude_ids,
            're_cat_ids': re_cat_ids,
            'year_required_ids': year_required_ids,
            'auto_choices': {
                'engine_types': AutoDetails.ENGINE_CHOICES,
                'transmissions': AutoDetails.TRANSMISSION_CHOICES,
                'body_types': AutoDetails.BODY_CHOICES,
            },
            'tire_season_choices': TireDetails.SEASON_CHOICES,
            're_deal_choices': RealEstateDetails.DEAL_CHOICES,
            'editing': True,
        }
        if extra:
            base.update(extra)
        return base

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()

        if len(title) < 3:
            messages.error(request, 'Nosaukums ir pārāk īss — minimums 3 rakstzīmes.')
            return render(request, 'listings/edit.html', ctx({'post': request.POST}))
        if len(title) > 200:
            messages.error(request, 'Nosaukums ir pārāk garš — maksimums 200 rakstzīmes.')
            return render(request, 'listings/edit.html', ctx({'post': request.POST}))
        if len(description) > 10000:
            messages.error(request, 'Apraksts ir pārāk garš — maksimums 10 000 rakstzīmes.')
            return render(request, 'listings/edit.html', ctx({'post': request.POST}))

        _, price_err = _validate_price(request.POST.get('price', ''))
        if price_err:
            messages.error(request, price_err)
            return render(request, 'listings/edit.html', ctx({'post': request.POST}))

        if contains_profanity(title) or contains_profanity(description):
            messages.error(request, 'Sludinājumā konstatēts nepiemērots saturs.')
            return render(request, 'listings/edit.html', ctx({'post': request.POST}))

        new_category = get_object_or_404(Category, pk=request.POST['category'])

        if _is_year_required_category(new_category) and not request.POST.get('year', '').strip():
            messages.error(request, 'Lūdzu norādiet izgatavošanas gadu.')
            return render(request, 'listings/edit.html', ctx({'post': request.POST}))

        listing.title = title
        listing.description = description
        listing.category = new_category
        listing.price = request.POST.get('price') or None
        listing.condition = request.POST.get('condition', 'used')
        listing.year = request.POST.get('year') or None
        listing.location = request.POST.get('location', '')
        listing.country = request.POST.get('country', '').strip()
        listing.city = request.POST.get('city', '').strip()
        listing.contact_email = request.POST.get('contact_email', '').strip()
        if _is_dating_category(new_category):
            listing.gender  = request.POST.get('gender', '')
            listing.seeking = request.POST.get('seeking', '')
        else:
            listing.gender  = ''
            listing.seeking = ''

        equipment_ids = request.POST.getlist('equipment')
        listing.equipment.set(Equipment.objects.filter(pk__in=equipment_ids))

        if _is_auto_category(new_category):
            _save_auto_details(listing, request.POST)
            TireDetails.objects.filter(listing=listing).delete()
            RealEstateDetails.objects.filter(listing=listing).delete()
        elif _is_tire_category(new_category):
            _save_tire_details(listing, request.POST)
            AutoDetails.objects.filter(listing=listing).delete()
            RealEstateDetails.objects.filter(listing=listing).delete()
        elif _is_re_category(new_category):
            _save_re_details(listing, request.POST)
            AutoDetails.objects.filter(listing=listing).delete()
            TireDetails.objects.filter(listing=listing).delete()
        else:
            AutoDetails.objects.filter(listing=listing).delete()
            TireDetails.objects.filter(listing=listing).delete()
            RealEstateDetails.objects.filter(listing=listing).delete()

        # Jaunas bildes (ja augšupielādētas) — servera validācija
        new_images = request.FILES.getlist('images')
        if new_images:
            _ALLOWED_IMG = {'image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/heic', 'image/heif'}
            _MAX_IMG_SIZE = 10 * 1024 * 1024
            if len(new_images) > 8:
                messages.error(request, 'Maksimums 8 bildes atļautas.')
                return render(request, 'listings/edit.html', ctx())
            for _img in new_images:
                if _img.content_type not in _ALLOWED_IMG:
                    messages.error(request, f'Atbalstīti tikai JPG, PNG, WEBP formāti ({_img.name}).')
                    return render(request, 'listings/edit.html', ctx())
                if _img.size > _MAX_IMG_SIZE:
                    messages.error(request, f'Bilde pārāk liela — maks. 10 MB ({_img.name}).')
                    return render(request, 'listings/edit.html', ctx())
            listing.images.all().delete()
            for i, img in enumerate(new_images):
                ListingImage.objects.create(listing=listing, image=img, order=i)

        # Jauns video (ja augšupielādēts)
        video_file = request.FILES.get('video')
        if video_file:
            allowed_ext = ('.mp4', '.webm', '.mov', '.avi', '.mkv')
            allowed_ct = ['video/mp4', 'video/webm', 'video/quicktime', 'video/avi', 'video/x-matroska']
            if video_file.content_type in allowed_ct or video_file.name.lower().endswith(allowed_ext):
                try:
                    listing.video.delete()
                except Exception:
                    pass
                ListingVideo.objects.create(listing=listing, file=video_file)

        listing.save()
        messages.success(request, 'Sludinājums atjaunināts.')
        return redirect('listing_detail', pk=listing.pk)

    return render(request, 'listings/edit.html', ctx())


@login_required
def delete_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user, is_auction=False)
    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'Sludinājums dzēsts.')
        return redirect('profile')
    return redirect('profile')


@login_required
def extend_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    if request.method == 'POST':
        days = int(request.POST.get('duration', 7))
        if days not in [7, 14, 21, 28]:
            days = 7
        base = max(listing.expires_at, timezone.now()) if listing.expires_at else timezone.now()
        listing.expires_at = base + timedelta(days=days)
        listing.is_active = True
        listing.save()
        messages.success(request, f'Sludinājums pagarināts līdz {listing.expires_at.strftime("%d.%m.%Y")}.')
        return redirect('listing_detail', pk=pk)
    return render(request, 'listings/extend.html', {
        'listing': listing,
        'duration_choices': DURATION_CHOICES,
    })


@login_required
def publish_template(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user, is_template=True)
    if request.method == 'POST':
        days = int(request.POST.get('duration', 7))
        if days not in [7, 14, 21, 28]:
            days = 7
        listing.is_active = True
        listing.is_template = False
        listing.template_created_at = None
        listing.expires_at = timezone.now() + timedelta(days=days)
        listing.moderation_status = 'approved'
        listing.views = 0
        listing.save()
        messages.success(request, 'Sludinājums publicēts no šablona.')
        return redirect('listing_detail', pk=pk)
    return render(request, 'listings/publish_template.html', {
        'listing': listing,
        'duration_choices': DURATION_CHOICES,
    })


@login_required
def delete_template(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user, is_template=True)
    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'Šablons dzēsts.')
    return redirect('profile')


@login_required
def mark_sold(request, pk):
    from django.contrib.auth.models import User as AuthUser
    from accounts.models import Notification
    listing = get_object_or_404(Listing, pk=pk, seller=request.user, is_auction=False)
    if request.method != 'POST':
        return redirect('listing_detail', pk=pk)
    buyer_username = request.POST.get('buyer_username', '').strip()
    buyer = None
    if buyer_username:
        try:
            buyer = AuthUser.objects.get(username=buyer_username)
            if buyer == request.user:
                messages.error(request, 'Pircējs nevar būt tu pats.')
                return redirect('listing_detail', pk=pk)
        except AuthUser.DoesNotExist:
            messages.error(request, f'Lietotājs "{buyer_username}" nav atrasts.')
            return redirect('listing_detail', pk=pk)
    listing.is_sold = True
    listing.is_active = False
    listing.buyer = buyer
    listing.save()
    if buyer:
        Notification.objects.create(
            user=buyer,
            text=f'Pārdevējs atzīmēja darījumu par "{listing.title}" kā pabeigtu. Atstājiet atsauksmi!',
            link=f'/accounts/lietotajs/{listing.seller.username}/vertejums/?listing={listing.pk}',
        )
        Notification.objects.create(
            user=request.user,
            text=f'Sludinājums "{listing.title}" pārdots! Atstājiet atsauksmi par pircēju.',
            link=f'/accounts/lietotajs/{buyer.username}/vertejums/?listing={listing.pk}',
        )
    else:
        messages.success(request, 'Sludinājums atzīmēts kā pārdots.')
        return redirect('listing_detail', pk=pk)
    messages.success(request, 'Sludinājums atzīmēts kā pārdots! Atstājiet atsauksmi par pircēju.')
    return redirect('listing_detail', pk=pk)


@login_required
def listing_promote(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user, is_active=True)
    settings = SiteSettings.get()
    is_auction = listing.is_auction
    if is_auction:
        enabled = settings.featured_auction_enabled
        fee = settings.featured_auction_fee
    else:
        enabled = settings.featured_listing_enabled
        fee = settings.featured_listing_fee

    if not enabled or fee <= 0:
        messages.error(request, 'TOP pakalpojums pašlaik nav pieejams.')
        return redirect('listing_detail', pk=pk)

    from accounts.models import Wallet, WalletTransaction
    wallet, _ = Wallet.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if wallet.balance < fee:
            messages.error(request, f'Nepietiek līdzekļu makā. TOP maksa ir €{fee}. Jūsu atlikums: €{wallet.balance}.')
            return redirect('listing_detail', pk=pk)
        Listing.objects.filter(is_auction=is_auction, is_featured=True).update(is_featured=False, featured_at=None)
        listing.is_featured = True
        listing.featured_at = timezone.now()
        listing.save(update_fields=['is_featured', 'featured_at'])
        desc = 'TOP izsole' if is_auction else 'TOP sludinājums'
        WalletTransaction.make_spend(wallet, fee, description=desc, reference=f'TOP-{listing.pk}')
        messages.success(request, f'Sludinājums paaugstināts uz TOP vietu!')
        return redirect('listing_detail', pk=pk)

    return render(request, 'listings/promote.html', {
        'listing': listing,
        'fee': fee,
        'wallet': wallet,
    })


def _msg_rate_exceeded(sender, recipient):
    return Message.objects.filter(
        sender=sender,
        recipient=recipient,
        created_at__gte=timezone.now() - timedelta(hours=1),
    ).count() >= 6


@login_required
def contact_seller(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.user == listing.seller:
        messages.error(request, 'Nevarat sazināties ar sevi.')
        return redirect('listing_detail', pk=pk)
    if request.method == 'POST':
        content = request.POST.get('message', '').strip()
        if not content:
            messages.error(request, 'Lūdzu ievadiet ziņojumu.')
            return redirect('listing_detail', pk=pk)
        blocked = contains_contact_info(content)
        if blocked:
            messages.error(request, f'Ziņojums nedrīkst saturēt {blocked}. Sazinieties caur platformu.')
            return redirect('listing_detail', pk=pk)
        if _msg_rate_exceeded(request.user, listing.seller):
            messages.error(request, 'Esat sasniedzis ziņojumu limitu — maksimum 6 ziņojumi stundā vienam pārdevējam.')
            return redirect('listing_detail', pk=pk)
        Message.objects.create(
            listing=listing,
            sender=request.user,
            recipient=listing.seller,
            content=content,
        )
        from accounts.notifications import notify as _notify
        _notify(listing.seller, 'message',
                f'Jauna ziņa no {request.user.username} par "{listing.title}"',
                url=f'/saruna/{listing.pk}/{request.user.pk}/')
        messages.success(request, 'Ziņojums nosūtīts pārdevējam.')
        return redirect('conversation', listing_pk=pk, user_pk=listing.seller.pk)
    return redirect('listing_detail', pk=pk)


@login_required
def inbox(request):
    from django.db.models import Max, Q as Qm
    user = request.user
    all_msgs = Message.objects.filter(
        Q(sender=user) | Q(recipient=user)
    ).select_related('listing', 'sender', 'recipient').order_by('-created_at')

    # Grupē pa sarunām (listing + otrs lietotājs)
    seen = set()
    conversations = []
    for msg in all_msgs:
        other = msg.recipient if msg.sender == user else msg.sender
        key = (msg.listing_id, other.pk)
        if key not in seen:
            seen.add(key)
            unread = Message.objects.filter(
                listing=msg.listing, sender=other, recipient=user, is_read=False
            ).count()
            conversations.append({
                'listing': msg.listing,
                'other': other,
                'last_msg': msg,
                'unread': unread,
            })

    return render(request, 'listings/inbox.html', {'conversations': conversations})


@login_required
def conversation(request, listing_pk, user_pk):
    from django.contrib.auth.models import User as AuthUser
    listing = get_object_or_404(Listing, pk=listing_pk)
    other = get_object_or_404(AuthUser, pk=user_pk)
    user = request.user

    thread = Message.objects.filter(
        listing=listing
    ).filter(
        Q(sender=user, recipient=other) | Q(sender=other, recipient=user)
    ).select_related('sender', 'recipient')

    if user != listing.seller and not thread.exists():
        from django.http import Http404
        raise Http404

    # Atzīmē kā lasītus
    thread.filter(recipient=user, is_read=False).update(is_read=True)

    if request.method == 'POST':
        content = request.POST.get('message', '').strip()
        if content:
            blocked = contains_contact_info(content)
            if blocked:
                messages.error(request, f'Ziņojums nedrīkst saturēt {blocked}.')
            elif _msg_rate_exceeded(user, other):
                messages.error(request, 'Esat sasniedzis ziņojumu limitu — maksimum 6 ziņojumi stundā vienam pārdevējam.')
            else:
                Message.objects.create(
                    listing=listing,
                    sender=user,
                    recipient=other,
                    content=content,
                )
        return redirect('conversation', listing_pk=listing_pk, user_pk=user_pk)

    return render(request, 'listings/conversation.html', {
        'listing': listing,
        'other': other,
        'thread': thread,
    })


@login_required
def report_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, is_active=True)
    if request.user == listing.seller:
        messages.error(request, 'Nevarat ziņot par savu sludinājumu.')
        return redirect('listing_detail', pk=pk)
    if Report.objects.filter(listing=listing, reporter=request.user).exists():
        messages.warning(request, 'Jūs jau esat ziņojis par šo sludinājumu.')
        return redirect('listing_detail', pk=pk)
    if request.method == 'POST':
        Report.objects.create(
            listing=listing,
            reporter=request.user,
            reason=request.POST.get('reason', 'other'),
            details=request.POST.get('details', ''),
        )
        messages.success(request, 'Paldies! Ziņojums nosūtīts moderatoram.')
        return redirect('listing_detail', pk=pk)
    return render(request, 'listings/report.html', {
        'listing': listing,
        'reasons': Report.REASON_CHOICES,
    })


@user_passes_test(is_admin, login_url='/accounts/login/')
def moderation_panel(request):
    reports = Report.objects.filter(status='new').select_related('listing', 'reporter').annotate(
        report_count=Count('listing__reports')
    )
    all_reports = Report.objects.select_related('listing', 'reporter', 'resolved_by').order_by('-created_at')[:50]
    flagged_listings = Listing.objects.annotate(report_count=Count('reports')).filter(
        report_count__gt=0, is_active=True
    ).order_by('-report_count')[:20]
    pending_listings = Listing.objects.filter(moderation_status='pending').select_related('seller', 'category').order_by('-created_at')
    return render(request, 'moderation/panel.html', {
        'reports': reports,
        'all_reports': all_reports,
        'flagged_listings': flagged_listings,
        'pending_listings': pending_listings,
    })


@user_passes_test(is_admin, login_url='/accounts/login/')
def moderate_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    action = request.POST.get('action')
    note = request.POST.get('admin_note', '')

    if action == 'approve':
        listing.moderation_status = 'approved'
        listing.is_active = True
        listing.moderation_note = note or ''
        listing.save()
        Report.objects.filter(listing=listing, status='new').update(
            status='resolved', resolved_by=request.user, resolved_at=timezone.now()
        )
        messages.success(request, f'Sludinājums "{listing.title}" apstiprināts.')

    elif action == 'reject':
        listing.moderation_status = 'rejected'
        listing.is_active = False
        listing.moderation_note = note or 'Noraidīts moderācijas rezultātā.'
        listing.save()
        Report.objects.filter(listing=listing, status='new').update(
            status='resolved', resolved_by=request.user,
            resolved_at=timezone.now(), admin_note=note or 'Noraidīts.'
        )
        messages.warning(request, f'Sludinājums "{listing.title}" noraidīts.')

    elif action == 'deactivate':
        listing.is_active = False
        listing.save()
        Report.objects.filter(listing=listing, status='new').update(
            status='resolved', resolved_by=request.user,
            resolved_at=timezone.now(), admin_note=note or 'Sludinājums deaktivēts.'
        )
        messages.success(request, f'Sludinājums "{listing.title}" deaktivēts.')

    elif action == 'delete':
        title = listing.title
        listing.delete()  # CASCADE dzēš arī Reports, tāpēc update nav vajadzīgs
        messages.success(request, f'Sludinājums "{title}" dzēsts.')
        return redirect('moderation_panel')

    elif action == 'dismiss':
        Report.objects.filter(listing=listing, status='new').update(
            status='reviewed', resolved_by=request.user,
            resolved_at=timezone.now(), admin_note=note or 'Ziņojums noraidīts.'
        )
        messages.info(request, f'Ziņojumi par "{listing.title}" noraidīti.')

    return redirect('moderation_panel')


def address_autocomplete(request):
    query = request.GET.get('q', '').strip()
    if not query or len(query) < 2:
        return JsonResponse({'predictions': []})
    import urllib.request, urllib.parse, json as _json
    params = urllib.parse.urlencode({
        'q': query,
        'format': 'json',
        'limit': 6,
        'addressdetails': 1,
    })
    url = f'https://nominatim.openstreetmap.org/search?{params}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'eizsole.lv/1.0'})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = _json.loads(r.read())
        predictions = [
            {
                'description': p['display_name'],
                'lat': p['lat'],
                'lng': p['lon'],
                'city': p.get('address', {}).get('city') or p.get('address', {}).get('town') or p.get('address', {}).get('village', ''),
                'country': p.get('address', {}).get('country', ''),
            }
            for p in data
        ]
        return JsonResponse({'predictions': predictions})
    except Exception:
        return JsonResponse({'predictions': []})


def discount_code_check(request):
    code = request.GET.get('code', '').strip().upper()
    if not code:
        return JsonResponse({'valid': False, 'error': 'Nav ievadīts kods.'})
    try:
        obj = DiscountCode.objects.get(code__iexact=code)
    except DiscountCode.DoesNotExist:
        return JsonResponse({'valid': False, 'error': 'Kods nav atrasts.'})
    valid, err = obj.is_valid()
    if not valid:
        return JsonResponse({'valid': False, 'error': err})
    return JsonResponse({
        'valid': True,
        'discount_type': obj.discount_type,
        'discount_value': str(obj.discount_value),
        'label': str(obj),
    })


# ── VIN atskaite ────────────────────────────────────────────────────────────

from decimal import Decimal as D

VIN_PRICE_NET   = D('15.00')
VIN_VAT_RATE    = D('0.21')
VIN_PRICE_GROSS = (VIN_PRICE_NET * (1 + VIN_VAT_RATE)).quantize(D('0.01'))  # 18.15


@login_required
def vin_report(request, pk):
    listing = get_object_or_404(Listing, pk=pk, is_active=True)
    try:
        vin = listing.auto_details.vin.strip().upper()
    except Exception:
        messages.error(request, 'Šim sludinājumam nav VIN koda.')
        return redirect('listing_detail', pk=pk)

    if not vin or len(vin) != 17:
        messages.error(request, 'VIN kods nav derīgs.')
        return redirect('listing_detail', pk=pk)

    # Vai lietotājs jau ir saņēmis atskaiti par šo VIN (30 dienas)
    cutoff = timezone.now() - timedelta(days=30)
    existing = VinReport.objects.filter(
        purchased_by=request.user, vin=vin, created_at__gte=cutoff
    ).first()
    if existing and not existing.api_error:
        return render(request, 'listings/vin_report.html', {
            'listing': listing,
            'report': existing,
            'reused': True,
        })

    if request.method == 'POST':
        is_eu_vat = request.POST.get('is_eu_vat') == '1'
        eu_vat_number = request.POST.get('eu_vat_number', '').strip().upper()

        if is_eu_vat and len(eu_vat_number) < 5:
            messages.error(request, 'Lūdzu ievadiet derīgu ES PVN reģistrācijas numuru.')
            return redirect('listing_detail', pk=pk)

        price_net   = VIN_PRICE_NET
        vat_amount  = D('0.00') if is_eu_vat else (VIN_PRICE_NET * VIN_VAT_RATE).quantize(D('0.01'))
        price_total = price_net + vat_amount

        from accounts.models import Wallet, WalletTransaction
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        if wallet.balance < price_total:
            messages.error(request, f'Nepietiek līdzekļu makā. Nepieciešami €{price_total}. Atlikums: €{wallet.balance}.')
            return redirect('listing_detail', pk=pk)

        from .vin_service import fetch_report
        data = fetch_report(vin)
        api_error = data.get('error', '') if isinstance(data, dict) else 'Nezināma kļūda'
        if api_error:
            messages.error(request, f'VIN atskaites kļūda: {api_error}')
            return redirect('listing_detail', pk=pk)

        WalletTransaction.make_spend(
            wallet, price_total,
            description=f'VIN atskaite {vin}',
            reference=f'VIN-{vin}',
        )

        rep = VinReport.objects.create(
            vin=vin,
            listing=listing,
            purchased_by=request.user,
            price_net=price_net,
            vat_amount=vat_amount,
            price_total=price_total,
            is_eu_vat=is_eu_vat,
            eu_vat_number=eu_vat_number if is_eu_vat else '',
            report_data=data,
        )
        return render(request, 'listings/vin_report.html', {
            'listing': listing,
            'report': rep,
            'reused': False,
        })

    # GET — apstiprinājuma lapa
    return render(request, 'listings/vin_confirm.html', {
        'listing': listing,
        'vin': vin,
        'price_net': VIN_PRICE_NET,
        'price_gross': VIN_PRICE_GROSS,
        'vat_rate': int(VIN_VAT_RATE * 100),
    })


def compare_toggle(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    get_object_or_404(Listing, pk=pk, is_active=True)
    ids = request.session.get('compare_ids', [])
    if pk in ids:
        ids.remove(pk)
        added = False
    else:
        if len(ids) >= 4:
            return JsonResponse({'error': 'Var salīdzināt maks. 4 sludinājumus.'}, status=400)
        ids.append(pk)
        added = True
    request.session['compare_ids'] = ids
    request.session.modified = True
    return JsonResponse({'added': added, 'count': len(ids), 'ids': ids})


def compare_clear(request):
    request.session['compare_ids'] = []
    request.session.modified = True
    return JsonResponse({'count': 0})


def compare_page(request):
    ids = request.session.get('compare_ids', [])
    listings = list(
        Listing.objects.filter(pk__in=ids, is_active=True)
        .select_related('category', 'seller', 'seller__profile')
        .prefetch_related('images', 'auto_details', 'tire_details', 're_details')
    )
    listings.sort(key=lambda l: ids.index(l.pk) if l.pk in ids else 999)
    return render(request, 'listings/compare.html', {'listings': listings})


@login_required
def favorite_toggle(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    listing = get_object_or_404(Listing, pk=pk, is_active=True)
    fav, created = Favorite.objects.get_or_create(user=request.user, listing=listing)
    if not created:
        fav.delete()
    return JsonResponse({'favorited': created, 'count': listing.favorited_by.count()})


@login_required
def favorites_list(request):
    cutoff = timezone.now() - timedelta(days=30)
    favs = (Favorite.objects
            .filter(user=request.user, created_at__gte=cutoff)
            .select_related('listing', 'listing__category', 'listing__seller')
            .prefetch_related('listing__images'))
    return render(request, 'listings/favorites.html', {'favs': favs})


def privacy_policy(request):
    return render(request, 'listings/privacy_policy.html')


def facebook_data_deletion(request):
    return render(request, 'listings/facebook_data_deletion.html')


def terms(request):
    return render(request, 'listings/terms.html')


def faq(request):
    faqs = [
        {'q': 'Vai eizsole.lv ir bezmaksas?',
         'a': 'Jā, eizsole.lv ir pilnīgi bezmaksas gan pircējiem, gan pārdevējiem. Sludinājumu publicēšana, solīšana un ziņapmaiņa ar pārdevēju ir bez maksas.'},
        {'q': 'Kā publicēt sludinājumu eizsole.lv?',
         'a': 'Reģistrējieties vai piesakieties kontā → nospiediet "Publicēt" → aizpildiet informāciju (nosaukums, apraksts, cena, kategorija, atrašanās vieta) → pievienojiet fotogrāfijas → nospiediet "Publicēt". Sludinājums parādīsies pēc moderatora apstiprinājuma.'},
        {'q': 'Kā darbojas izsoles eizsole.lv?',
         'a': 'Izsole sākas ar minimālo cenu un beidzas noteiktā laikā. Uzvar tas, kurš piedāvājis augstāko cenu. Anti-snipe aizsardzība: ja solījums iesniegts pēdējās 60 sekundēs, izsoles laiks automātiski pagarinās par 3 minūtēm.'},
        {'q': 'Kā solīt izsolē?',
         'a': 'Atveriet izsoles lapu → piesakieties kontā → ievadiet solīšanas summu (ne mazāku par minimālo soli) → nospiediet "Solīt". Saņemsiet e-pasta paziņojumu, ja jūs pārsolīs.'},
        {'q': 'Kā sazināties ar pārdevēju?',
         'a': 'Katram sludinājumam ir poga "Sazināties". Nosūtiet ziņu tieši pārdevējam caur eizsole.lv iekšējo ziņapmaiņas sistēmu. Visas sarunas saglabājas jūsu profilā.'},
        {'q': 'Cik ilgi darbojas sludinājums?',
         'a': 'Sludinājums darbojas 30 dienas no publicēšanas brīža. Pēc tam to var pagarināt vai atkārtoti publicēt. Izsoles darbojas pārdevēja noteiktu laiku — parasti 3 līdz 14 dienas.'},
        {'q': 'Kādas kategorijas ir pieejamas?',
         'a': 'eizsole.lv piedāvā: Auto un transports, Nekustamais īpašums, Elektronikas un tehnika, Mājsaimniecība, Apģērbs un mode, Sports un hobiji, Lauksaimniecība, Celtniecība, Kolekcionēšana un daudz ko citu.'},
        {'q': 'Kā ziņot par aizdomīgu sludinājumu?',
         'a': 'Katram sludinājumam ir poga "Ziņot". Izvēlieties iemeslu un nosūtiet ziņojumu. Moderatori izskata ziņojumus 24 stundu laikā.'},
        {'q': 'Vai varu pārdot jebko?',
         'a': 'Nav atļauts pārdot: ieročus, narkotikas, viltotus produktus, dzīvniekus bez dokumentiem un jebko pretrunā Latvijas likumiem. Skatiet Lietošanas noteikumus.'},
        {'q': 'Vai eizsole.lv darbojas mobilajā tālrunī?',
         'a': 'Jā! eizsole.lv ir optimizēts mobilajām ierīcēm un instalējams kā lietotne (PWA) bez App Store. Nospiediet "Mobilā lietotne" mājaslapas apakšā.'},
    ]
    quick_links = [
        {'url': '/publicet/', 'icon': 'plus-circle', 'title': 'Publicēt sludinājumu', 'desc': 'Bezmaksas, 2 minūtes'},
        {'url': '/izsoles/', 'icon': 'hammer', 'title': 'Aktīvās izsoles', 'desc': 'Solī un uzvari'},
        {'url': '/meklet/', 'icon': 'search', 'title': 'Meklēt', 'desc': 'Atrodi ko meklē'},
        {'url': '/blogs/', 'icon': 'journal-text', 'title': 'Blogs', 'desc': 'Padomi un ceļveži'},
        {'url': '/privatuma-politika/', 'icon': 'shield-check', 'title': 'Privātuma politika', 'desc': 'Datu aizsardzība'},
        {'url': '/lietosanas-noteikumi/', 'icon': 'file-text', 'title': 'Lietošanas noteikumi', 'desc': 'Noteikumi un nosacījumi'},
    ]
    return render(request, 'listings/faq.html', {'faqs': faqs, 'quick_links': quick_links})


def robots_txt(request):
    from django.http import HttpResponse
    content = (
        "User-agent: *\n"
        "Disallow: /admin/\n"
        "Disallow: /accounts/\n"
        "Disallow: /moderacija/\n"
        f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml\n"
    )
    return HttpResponse(content, content_type='text/plain')


@login_required
def listing_stats(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    from django.db.models import Count
    from django.db.models.functions import TruncDate
    import json

    today = timezone.now().date()
    since_14 = today - timedelta(days=13)

    # Skatījumi pa dienām (pēdējās 14 dienas)
    daily_qs = (
        ListingView.objects
        .filter(listing=listing, viewed_at__date__gte=since_14)
        .annotate(day=TruncDate('viewed_at'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )
    daily_map = {str(row['day']): row['count'] for row in daily_qs}
    days = [(since_14 + timedelta(days=i)) for i in range(14)]
    chart_labels = [d.strftime('%-d.%-m') for d in days]
    chart_data = [daily_map.get(str(d), 0) for d in days]

    # Avoti
    source_qs = (
        ListingView.objects
        .filter(listing=listing)
        .values('source')
        .annotate(count=Count('id'))
    )
    source_labels_map = {'google': 'Google', 'facebook': 'Facebook', 'internal': 'Eizsole.lv', 'direct': 'Tiešā', 'other': 'Cits'}
    source_data = {source_labels_map.get(r['source'], r['source']): r['count'] for r in source_qs}

    return render(request, 'listings/stats.html', {
        'listing': listing,
        'views_total': listing.views,
        'views_7d': sum(daily_map.get(str(today - timedelta(days=i)), 0) for i in range(7)),
        'views_30d': ListingView.objects.filter(listing=listing, viewed_at__date__gte=today - timedelta(days=29)).count(),
        'favorites': listing.favorited_by.count(),
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        'source_data': json.dumps(source_data),
    })


@login_required
def save_search(request):
    if request.method != 'POST':
        return redirect('search')
    if SavedSearch.objects.filter(user=request.user).count() >= 10:
        messages.warning(request, 'Varat saglabāt līdz 10 meklēšanām.')
        return redirect(request.POST.get('next', 'search'))

    cat_pk = request.POST.get('category', '')
    category = None
    if cat_pk:
        try:
            category = Category.objects.get(pk=cat_pk)
        except Category.DoesNotExist:
            pass

    SavedSearch.objects.create(
        user=request.user,
        query=request.POST.get('query', '').strip()[:200],
        price_min=request.POST.get('price_min', '').strip()[:20],
        price_max=request.POST.get('price_max', '').strip()[:20],
        condition=request.POST.get('condition', '').strip()[:10],
        category=category,
        listing_type=request.POST.get('listing_type', '').strip()[:10],
    )
    messages.success(request, 'Meklēšana saglabāta! Jūs saņemsiet e-pastu, kad parādīsies jauni sludinājumi.')
    return redirect(request.POST.get('next', 'search'))


@login_required
def delete_saved_search(request, pk):
    saved = get_object_or_404(SavedSearch, pk=pk, user=request.user)
    saved.delete()
    messages.success(request, 'Saglabātā meklēšana dzēsta.')
    return redirect('saved_searches')


@login_required
def saved_searches(request):
    searches = SavedSearch.objects.filter(user=request.user)
    return render(request, 'listings/saved_searches.html', {'searches': searches})
