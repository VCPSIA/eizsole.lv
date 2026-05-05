from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from listings.models import Listing


class Auction(models.Model):
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE, related_name='auction')
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    min_bid_increment = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    buy_now_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    reserve_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ends_at = models.DateTimeField()
    winner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='won_auctions')
    is_finished = models.BooleanField(default=False)
    anti_snipe_count = models.PositiveSmallIntegerField(default=0)  # cik reizes pagarināta

    def __str__(self):
        return f"Izsole: {self.listing.title}"

    def is_active(self):
        return not self.is_finished and self.ends_at > timezone.now()

    def time_left(self):
        if self.is_active():
            return self.ends_at - timezone.now()
        return None

    def bid_count(self):
        return self.bids.count()

    def reserve_met(self):
        if not self.reserve_price:
            return True
        return self.current_price >= self.reserve_price

    def leading_bidder(self):
        top = self.bids.order_by('-amount').first()
        return top.bidder if top else None


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    placed_at = models.DateTimeField(auto_now_add=True)
    is_auto = models.BooleanField(default=False)  # atzīme automātiskajiem solījumiem

    class Meta:
        ordering = ['-amount']

    def __str__(self):
        return f"{self.bidder.username} — €{self.amount}"


class ProxyBid(models.Model):
    """Lietotāja automātiskais solījums ar maksimālo summu."""
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='proxy_bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proxy_bids')
    max_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-max_amount']

    def __str__(self):
        return f"Proxy: {self.bidder.username} max €{self.max_amount}"
