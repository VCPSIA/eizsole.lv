from django.contrib import admin
from .models import Auction, Bid


class BidInline(admin.TabularInline):
    model = Bid
    extra = 0
    readonly_fields = ['bidder', 'amount', 'placed_at']


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ['listing', 'starting_price', 'current_price', 'ends_at', 'is_finished']
    list_filter = ['is_finished']
    inlines = [BidInline]
