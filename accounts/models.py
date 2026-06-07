import secrets
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

VAT_RATE = Decimal('0.21')


class Notification(models.Model):
    TYPE_CHOICES = [
        ('bid',     'Jauns solījums'),
        ('message', 'Jauna ziņa'),
        ('expiry',  'Sludinājums beidzas'),
        ('outbid',  'Pārsolīts'),
        ('won',     'Izsole uzvarēta'),
    ]
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notif_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    text       = models.CharField(max_length=300)
    url        = models.CharField(max_length=300, blank=True)
    is_read    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username}: {self.text[:50]}'


class Profile(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('private', 'Privātpersona'),
        ('company', 'Uzņēmums'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES, default='private')

    # Privātpersona
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    personal_code = models.CharField(max_length=20, blank=True, verbose_name='Personas kods')

    # Uzņēmums
    company_name = models.CharField(max_length=200, blank=True, verbose_name='Uzņēmuma nosaukums')
    reg_number = models.CharField(max_length=20, blank=True, verbose_name='Reģistrācijas numurs')
    vat_number = models.CharField(max_length=20, blank=True, verbose_name='PVN reģistrācijas numurs')
    legal_address = models.CharField(max_length=200, blank=True, verbose_name='Juridiskā adrese')
    contact_person = models.CharField(max_length=100, blank=True, verbose_name='Kontaktpersona')

    # Kopīgi
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True, verbose_name='Adrese')
    location = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True, verbose_name='Valsts')
    city = models.CharField(max_length=100, blank=True, verbose_name='Pilsēta')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)

    def display_name(self):
        if self.account_type == 'company' and self.company_name:
            return self.company_name
        if self.first_name or self.last_name:
            return f'{self.first_name} {self.last_name}'.strip()
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            try:
                from listings.image_utils import compress_image
                compress_image(self.avatar)
            except Exception:
                pass

    def __str__(self):
        return f"Profils: {self.user.username}"


class EmailVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_verifications')
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def is_valid(self):
        return not self.is_used and timezone.now() < self.created_at + timedelta(hours=24)

    @classmethod
    def create_for_user(cls, user):
        cls.objects.filter(user=user, is_used=False).update(is_used=True)
        return cls.objects.create(user=user, token=secrets.token_urlsafe(32))

    def __str__(self):
        return f"E-pasta verifikācija: {self.user.username}"


class PhoneVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='phone_verifications')
    phone = models.CharField(max_length=20)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def is_valid(self):
        return not self.is_used and timezone.now() < self.created_at + timedelta(minutes=10)

    @classmethod
    def create_for_user(cls, user, phone):
        cls.objects.filter(user=user, is_used=False).update(is_used=True)
        import random
        code = str(random.randint(100000, 999999))
        return cls.objects.create(user=user, phone=phone, code=code)

    def __str__(self):
        return f"Telefona verifikācija: {self.user.username} ({self.phone})"


class AccountDeletionRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='deletion_request')
    email_token = models.CharField(max_length=64, unique=True)
    sms_code = models.CharField(max_length=6)
    email_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.created_at + timedelta(hours=1)

    @classmethod
    def create_for_user(cls, user):
        import random
        cls.objects.filter(user=user).delete()
        return cls.objects.create(
            user=user,
            email_token=secrets.token_urlsafe(32),
            sms_code=str(random.randint(100000, 999999)),
        )

    def __str__(self):
        return f"Konta dzēšana: {self.user.username}"


class EmailChangeRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_change_requests')
    new_email = models.EmailField()
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def is_valid(self):
        return not self.is_used and timezone.now() < self.created_at + timedelta(hours=24)

    @classmethod
    def create_for_user(cls, user, new_email):
        cls.objects.filter(user=user, is_used=False).update(is_used=True)
        return cls.objects.create(user=user, new_email=new_email, token=secrets.token_urlsafe(32))

    def __str__(self):
        return f"E-pasta maiņa: {self.user.username} → {self.new_email}"


class Rating(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_given')
    reviewed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_received')
    listing = models.ForeignKey(
        'listings.Listing', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='ratings',
    )
    auction = models.OneToOneField(
        'auctions.Auction', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='rating',
    )
    stars = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField(blank=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reviewer', 'reviewed', 'listing')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.reviewer.username} → {self.reviewed.username}: {self.stars}★'

    def save(self, *args, **kwargs):
        self.stars = max(1, min(5, self.stars))
        super().save(*args, **kwargs)
        from django.db.models import Avg
        avg = Rating.objects.filter(reviewed=self.reviewed).aggregate(a=Avg('stars'))['a'] or 0
        Profile.objects.filter(user=self.reviewed).update(rating=round(avg, 2))

    def delete(self, *args, **kwargs):
        reviewed = self.reviewed
        super().delete(*args, **kwargs)
        from django.db.models import Avg
        avg = Rating.objects.filter(reviewed=reviewed).aggregate(a=Avg('stars'))['a'] or 0
        Profile.objects.filter(user=reviewed).update(rating=round(avg, 2))


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)

    def total_deposited(self):
        return self.transactions.filter(tx_type='deposit').aggregate(
            t=models.Sum('amount'))['t'] or Decimal('0.00')

    def total_spent(self):
        return self.transactions.filter(tx_type='spend').aggregate(
            t=models.Sum('amount'))['t'] or Decimal('0.00')

    def __str__(self):
        return f"Maks: {self.user.username} (€{self.balance})"


class WalletTransaction(models.Model):
    TYPE_CHOICES = [
        ('deposit', 'Iemaksa'),
        ('spend',   'Tēriņš'),
        ('refund',  'Atmaksa'),
    ]
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    tx_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200, blank=True)
    reference = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @classmethod
    def make_deposit(cls, wallet, amount_with_vat, reference=''):
        vat = (amount_with_vat * VAT_RATE / (1 + VAT_RATE)).quantize(Decimal('0.01'))
        tx = cls.objects.create(
            wallet=wallet, tx_type='deposit',
            amount=amount_with_vat, vat_amount=vat,
            description='Maka papildināšana', reference=reference,
        )
        wallet.balance += amount_with_vat
        wallet.save()
        return tx

    @classmethod
    def make_spend(cls, wallet, amount_with_vat, description='', reference=''):
        vat = (amount_with_vat * VAT_RATE / (1 + VAT_RATE)).quantize(Decimal('0.01'))
        tx = cls.objects.create(
            wallet=wallet, tx_type='spend',
            amount=amount_with_vat, vat_amount=vat,
            description=description, reference=reference,
        )
        wallet.balance -= amount_with_vat
        wallet.save()
        return tx

    def __str__(self):
        return f"{self.get_tx_type_display()} €{self.amount} — {self.wallet.user.username}"
