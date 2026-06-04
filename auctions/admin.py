from django.contrib import admin
from django.utils import timezone
from django.contrib import messages
from .models import Auction, Bid, CentAuctionEscrow


class BidInline(admin.TabularInline):
    model = Bid
    extra = 0
    readonly_fields = ['bidder', 'amount', 'placed_at']


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ['listing', 'auction_type', 'is_cent_auction', 'starting_price', 'current_price', 'ends_at', 'is_finished']
    list_filter = ['is_finished', 'auction_type', 'is_cent_auction']
    inlines = [BidInline]


@admin.register(CentAuctionEscrow)
class CentAuctionEscrowAdmin(admin.ModelAdmin):
    list_display  = ['pk', 'auction_title', 'amount', 'commission_total', 'net_to_seller', 'status', 'created_at', 'released_at']
    list_filter   = ['status']
    readonly_fields = [
        'auction', 'amount', 'commission', 'vat_amount', 'net_to_seller',
        'created_at', 'shipped_at', 'delivered_at', 'released_at',
    ]
    fields = [
        'auction', 'status',
        'amount', 'commission', 'vat_amount', 'net_to_seller',
        'tracking_info', 'note',
        'created_at', 'shipped_at', 'delivered_at', 'released_at',
    ]
    actions = ['action_release', 'action_refund', 'action_dispute']

    def auction_title(self, obj):
        return obj.auction.listing.title[:60]
    auction_title.short_description = 'Izsole'

    def commission_total(self, obj):
        return f'€{obj.commission + obj.vat_amount}'
    commission_total.short_description = 'Komisija+PVN'

    @admin.action(description='✅ Atbrīvot escrow → pārdevājam')
    def action_release(self, request, queryset):
        from auctions.views import _release_escrow_to_seller
        released = 0
        for escrow in queryset.filter(status__in=['held', 'shipped', 'delivered']):
            _release_escrow_to_seller(escrow)
            released += 1
        self.message_user(request, f'{released} escrow atbrīvots pārdevājam.', messages.SUCCESS)

    @admin.action(description='↩ Atmaksāt pircējam')
    def action_refund(self, request, queryset):
        from accounts.models import Wallet, WalletTransaction
        from accounts.notifications import notify
        refunded = 0
        for escrow in queryset.filter(status__in=['held', 'shipped']):
            winner = escrow.auction.winner
            if winner:
                wallet, _ = Wallet.objects.get_or_create(user=winner)
                ref = f'escrow_refund_{escrow.pk}'
                if not WalletTransaction.objects.filter(reference=ref).exists():
                    WalletTransaction.make_deposit(
                        wallet, escrow.amount, reference=ref,
                    )
                    WalletTransaction.objects.filter(reference=ref).update(
                        description=f'Atmaksa (escrow): {escrow.auction.listing.title[:70]}'
                    )
                    notify(winner, 'bid',
                           f'Jūsu maksājums €{escrow.amount} par "{escrow.auction.listing.title}" '
                           f'atmaksāts pēc administratora lēmuma.',
                           url=f'/izsoles/{escrow.auction.pk}/')
            escrow.status = 'refunded'
            escrow.released_at = timezone.now()
            escrow.save()
            refunded += 1
        self.message_user(request, f'{refunded} escrow atmaksāts pircājam.', messages.WARNING)

    @admin.action(description='⚠️ Atzīmēt kā strīdu')
    def action_dispute(self, request, queryset):
        updated = queryset.filter(status__in=['held', 'shipped']).update(status='disputed')
        self.message_user(request, f'{updated} escrow atzīmēts kā strīds.', messages.WARNING)
