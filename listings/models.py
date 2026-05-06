from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['order', 'pk']

    def __str__(self):
        return self.name


class Listing(models.Model):
    CONDITION_CHOICES = [
        ('new', 'Jauns'),
        ('used', 'Lietots'),
        ('damaged', 'Bojāts'),
    ]
    DEAL_TYPE_CHOICES = [
        ('sell',  'Pārdod'),
        ('buy',   'Pērk'),
        ('trade', 'Maina'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='listings')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='used')
    deal_type = models.CharField(max_length=5, choices=DEAL_TYPE_CHOICES, blank=True, default='')
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True, verbose_name='Valsts')
    city = models.CharField(max_length=100, blank=True, verbose_name='Pilsēta')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    MODERATION_CHOICES = [
        ('approved', 'Apstiprināts'),
        ('pending',  'Gaida apstiprināšanu'),
        ('rejected', 'Noraidīts'),
    ]
    is_active = models.BooleanField(default=True)
    is_auction = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    moderation_status = models.CharField(max_length=10, choices=MODERATION_CHOICES, default='approved')
    moderation_note = models.TextField(blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    is_featured = models.BooleanField(default=False, verbose_name='TOP sludinājums')
    featured_at = models.DateTimeField(null=True, blank=True)
    equipment = models.ManyToManyField('Equipment', blank=True, related_name='listings')

    def __str__(self):
        return self.title

    def get_main_image(self):
        return self.images.first()


class Equipment(models.Model):
    GROUP_CHOICES = [
        ('comfort', 'Komforts'),
        ('safety', 'Drošība'),
        ('media', 'Mediji un navigācija'),
        ('tech', 'Tehnika'),
        ('extra', 'Papildus'),
    ]
    name = models.CharField(max_length=100)
    group = models.CharField(max_length=20, choices=GROUP_CHOICES)
    icon = models.CharField(max_length=50, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['group', 'order', 'name']

    def __str__(self):
        return self.name


class AutoDetails(models.Model):
    ENGINE_CHOICES = [
        ('petrol',   'Benzīns'),
        ('diesel',   'Dīzelis'),
        ('electric', 'Elektro'),
        ('hybrid',   'Hibrīds'),
        ('gas',      'Gāze'),
        ('other',    'Cits'),
    ]
    TRANSMISSION_CHOICES = [
        ('manual',    'Manuālā'),
        ('automatic', 'Automātiskā'),
        ('robot',     'Robots / Pus-automāts'),
        ('cvt',       'Variators (CVT)'),
    ]
    BODY_CHOICES = [
        ('sedan',       'Sedans'),
        ('hatchback',   'Hečbeks'),
        ('wagon',       'Universāls'),
        ('suv',         'SUV / Apvidus'),
        ('coupe',       'Kupeja'),
        ('convertible', 'Kabriolets'),
        ('minivan',     'Minivens'),
        ('pickup',      'Pikaps'),
        ('van',         'Furgons'),
        ('other',       'Cits'),
    ]

    listing = models.OneToOneField(Listing, on_delete=models.CASCADE, related_name='auto_details')
    engine_type = models.CharField(max_length=10, choices=ENGINE_CHOICES)
    engine_volume = models.DecimalField(max_digits=4, decimal_places=1)
    transmission = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES)
    body_type = models.CharField(max_length=12, choices=BODY_CHOICES)
    mileage = models.PositiveIntegerField(default=0, verbose_name='Nobraukums (km)')
    has_inspection = models.BooleanField(default=True)
    inspection_date = models.DateField(null=True, blank=True)
    reg_number = models.CharField(max_length=15, verbose_name='Reģ. numurs')
    vin = models.CharField(max_length=17, verbose_name='VIN kods')

    def __str__(self):
        return f'Auto dati: {self.listing.title}'


class RealEstateDetails(models.Model):
    DEAL_CHOICES = [
        ('sell',  'Pārdod'),
        ('buy',   'Pērk'),
        ('trade', 'Maina'),
        ('rent',  'Izīrē'),
        ('lease', 'Īrē'),
    ]

    listing = models.OneToOneField(Listing, on_delete=models.CASCADE, related_name='re_details')
    deal_type = models.CharField(max_length=5, choices=DEAL_CHOICES, verbose_name='Darījuma veids')
    country = models.CharField(max_length=100, verbose_name='Valsts')
    district = models.CharField(max_length=100, verbose_name='Rajons')
    city = models.CharField(max_length=100, verbose_name='Pilsēta')

    def __str__(self):
        return f'NĪ dati: {self.listing.title}'


class TireDetails(models.Model):
    SEASON_CHOICES = [
        ('summer',     'Vasaras'),
        ('winter',     'Ziemas'),
        ('allseason',  'Vissezonas'),
        ('studded',    'Ziemas ar nagliņām'),
    ]

    listing = models.OneToOneField(Listing, on_delete=models.CASCADE, related_name='tire_details')
    radius = models.PositiveSmallIntegerField(verbose_name='Rādiuss (collas)')
    width = models.PositiveSmallIntegerField(verbose_name='Platums (mm)')
    profile = models.PositiveSmallIntegerField(verbose_name='Profils (%)')
    season = models.CharField(max_length=10, choices=SEASON_CHOICES, verbose_name='Sezona')
    manufacturer = models.CharField(max_length=100, verbose_name='Ražotājs')
    load_index = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Slodzes indekss')
    speed_index = models.CharField(max_length=3, blank=True, verbose_name='Ātruma indekss')

    def __str__(self):
        return f'Riepas dati: {self.listing.title}'


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listings/%Y/%m/')
    is_main = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Bilde: {self.listing.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            try:
                from .image_utils import compress_image
                compress_image(self.image)
            except Exception:
                pass


class ListingVideo(models.Model):
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE, related_name='video')
    file = models.FileField(upload_to='listings/videos/%Y/%m/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video: {self.listing.title}"


class Message(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender} → {self.recipient}: {self.content[:40]}'


class Report(models.Model):
    REASON_CHOICES = [
        ('spam', 'Surogātpasts / atkārtots sludinājums'),
        ('fraud', 'Krāpniecība / viltojums'),
        ('wrong_category', 'Nepareiza kategorija'),
        ('inappropriate', 'Nepiemērots saturs'),
        ('illegal', 'Nelikumīgs saturs'),
        ('other', 'Cits iemesls'),
    ]
    STATUS_CHOICES = [
        ('new', 'Jauns'),
        ('reviewed', 'Izskatīts'),
        ('resolved', 'Atrisināts'),
    ]

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reports_made')
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    details = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports_resolved')
    resolved_at = models.DateTimeField(null=True, blank=True)
    admin_note = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Ziņojums: {self.listing.title} ({self.get_reason_display()})"


class DiscountCode(models.Model):
    TYPE_CHOICES = [
        ('percent', 'Procenti (%)'),
        ('fixed',   'Fiksēta summa (€)'),
    ]
    code = models.CharField(max_length=30, unique=True, verbose_name='Kods')
    discount_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='percent', verbose_name='Atlaides veids')
    discount_value = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Atlaides vērtība')
    max_uses = models.PositiveIntegerField(null=True, blank=True, verbose_name='Maks. izmantošanu reizes (tukšs = neierobežots)')
    used_count = models.PositiveIntegerField(default=0, verbose_name='Izmantots reizes')
    valid_from = models.DateTimeField(null=True, blank=True, verbose_name='Derīgs no')
    valid_until = models.DateTimeField(null=True, blank=True, verbose_name='Derīgs līdz')
    is_active = models.BooleanField(default=True, verbose_name='Aktīvs')

    class Meta:
        verbose_name = 'Atlaižu kods'
        verbose_name_plural = 'Atlaižu kodi'
        ordering = ['-id']

    def __str__(self):
        if self.discount_type == 'percent':
            return f'{self.code} — {self.discount_value}%'
        return f'{self.code} — €{self.discount_value}'

    def is_valid(self):
        from django.utils import timezone as tz
        if not self.is_active:
            return False, 'Kods nav aktīvs.'
        if self.max_uses is not None and self.used_count >= self.max_uses:
            return False, 'Kods ir jau izmantots maksimālais reižu skaits.'
        now = tz.now()
        if self.valid_from and now < self.valid_from:
            return False, 'Kods vēl nav derīgs.'
        if self.valid_until and now > self.valid_until:
            return False, 'Koda derīguma termiņš ir beidzies.'
        return True, ''

    def apply(self, amount):
        """Aprēķina atlaidi — atgriež (discounted_amount, saved_amount)."""
        from decimal import Decimal
        if self.discount_type == 'percent':
            pct = min(self.discount_value, Decimal('100'))
            saved = (amount * pct / Decimal('100')).quantize(Decimal('0.01'))
        else:
            saved = min(self.discount_value, amount)
        return max(amount - saved, Decimal('0.00')), saved


class VinReport(models.Model):
    vin = models.CharField(max_length=17, db_index=True)
    listing = models.ForeignKey('Listing', on_delete=models.SET_NULL, null=True, blank=True, related_name='vin_reports')
    purchased_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='vin_reports')
    price_net = models.DecimalField(max_digits=8, decimal_places=2)
    vat_amount = models.DecimalField(max_digits=8, decimal_places=2)
    price_total = models.DecimalField(max_digits=8, decimal_places=2)
    is_eu_vat = models.BooleanField(default=False)
    eu_vat_number = models.CharField(max_length=30, blank=True)
    report_data = models.JSONField(null=True, blank=True)
    api_error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'VIN {self.vin} — {self.purchased_by}'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} ♥ {self.listing.title}'


class SiteSettings(models.Model):
    listing_fee_enabled = models.BooleanField(default=False, verbose_name='Maksa par sludinājumu ieslēgta')
    listing_fee = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'), verbose_name='Sludinājuma maksa (€ ar PVN)')
    auction_fee_enabled = models.BooleanField(default=False, verbose_name='Maksa par izsoli ieslēgta')
    auction_fee = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'), verbose_name='Izsoles maksa (€ ar PVN)')
    featured_listing_enabled = models.BooleanField(default=False, verbose_name='TOP sludinājums ieslēgts')
    featured_listing_fee = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'), verbose_name='TOP sludinājuma maksa (€ ar PVN)')
    featured_auction_enabled = models.BooleanField(default=False, verbose_name='TOP izsole ieslēgta')
    featured_auction_fee = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'), verbose_name='TOP izsoles maksa (€ ar PVN)')
    banner_enabled = models.BooleanField(default=False, verbose_name='Baneri ieslēgti')
    banner_fee = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'), verbose_name='Banera maksa (€ ar PVN)')
    banner_rotation_seconds = models.PositiveIntegerField(default=5, verbose_name='Banera rotācijas laiks (sekundes)')

    class Meta:
        verbose_name = 'Vietnes iestatījumi'
        verbose_name_plural = 'Vietnes iestatījumi'

    def __str__(self):
        return 'Vietnes iestatījumi'

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Banner(models.Model):
    listing = models.OneToOneField('Listing', on_delete=models.CASCADE, related_name='banner', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='banners')
    image = models.ImageField(upload_to='banners/', verbose_name='Attēls')
    text = models.CharField(max_length=200, blank=True, verbose_name='Teksts (rakstāmmašīna)')
    link_url = models.URLField(blank=True, verbose_name='Saite (pēc klikšķa)')
    is_active = models.BooleanField(default=True, verbose_name='Aktīvs')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Baneris'
        verbose_name_plural = 'Baneri'
        ordering = ['created_at']

    def __str__(self):
        return f'Baneris #{self.pk} — {self.user.username}'
