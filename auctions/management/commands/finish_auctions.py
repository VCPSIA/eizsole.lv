from django.core.management.base import BaseCommand
from django.utils import timezone
from auctions.models import Auction, ProxyBid
from accounts.models import Wallet, WalletTransaction
from accounts.notifications import notify


class Command(BaseCommand):
    help = 'Pabeidz visas beigtās izsoles un iekasē maksu no uzvarētājiem'

    def handle(self, *args, **options):
        expired = Auction.objects.filter(is_finished=False, ends_at__lte=timezone.now())
        count = expired.count()

        for auction in expired:
            top_bid = auction.bids.order_by('-amount').first()

            if top_bid and auction.reserve_met():
                winner = top_bid.bidder
                amount = auction.current_price
                wallet, _ = Wallet.objects.get_or_create(user=winner)

                ref = f'auction_{auction.pk}'
                if not WalletTransaction.objects.filter(reference=ref).exists():
                    if wallet.balance >= amount:
                        WalletTransaction.make_spend(
                            wallet, amount,
                            description=f'Izsole: {auction.listing.title[:80]}',
                            reference=ref,
                        )
                        notify(winner, 'won',
                               f'Apsveicam! Uzvarējāt izsolē "{auction.listing.title}" par €{amount}. '
                               f'€{amount} norakstīti no maka.',
                               url=f'/izsoles/{auction.pk}/')
                        self.stdout.write(f'  ✓ {auction} → {winner.username} €{amount} (samaksāts)')
                    else:
                        notify(winner, 'won',
                               f'Uzvarējāt izsolē "{auction.listing.title}" par €{amount}, '
                               f'taču maka atlikums nepietiek (€{wallet.balance:.2f}). '
                               f'Lūdzu papildiniet maku!',
                               url='/accounts/maks/papildinat/')
                        self.stdout.write(f'  ! {auction} → {winner.username} €{amount} (maks nepietiek)')

                auction.winner = winner
                notify(auction.listing.seller, 'bid',
                       f'Izsole "{auction.listing.title}" beigusies. '
                       f'Uzvarētājs: {winner.username} (€{amount}).',
                       url=f'/izsoles/{auction.pk}/')
            else:
                notify(auction.listing.seller, 'bid',
                       f'Izsole "{auction.listing.title}" beigusies bez uzvarētāja.',
                       url=f'/izsoles/{auction.pk}/')
                self.stdout.write(f'  - {auction} → bez uzvarētāja')

            auction.is_finished = True
            auction.listing.is_active = False
            auction.listing.save()
            auction.save()
            ProxyBid.objects.filter(auction=auction, is_active=True).update(is_active=False)

        self.stdout.write(self.style.SUCCESS(f'Pabeigtas {count} izsoles.'))
