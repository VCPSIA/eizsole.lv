from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from auctions.models import Auction
from listings.models import Listing
from accounts.notifications import _send_email


def _window(hours):
    """Laika logs ±5 min ap norādīto stundu skaitu no tagad."""
    now = timezone.now()
    return now + timedelta(hours=hours) - timedelta(minutes=5), \
           now + timedelta(hours=hours) + timedelta(minutes=5)


class Command(BaseCommand):
    help = 'Sūta atgādinājumu e-pastus par tuvojošiem notikumiem'

    def handle(self, *args, **options):
        sent = 0

        # --- Izsoles beidzas pēc 1 stundas ---
        lo, hi = _window(1)
        soon_1h = Auction.objects.filter(
            is_finished=False, ends_at__range=(lo, hi)
        ).select_related('listing__seller')

        for auction in soon_1h:
            title = auction.listing.title
            url = f'/izsoles/{auction.pk}/'
            ends = auction.ends_at.strftime('%H:%M')

            # Vadošajam solītājam
            top = auction.bids.order_by('-amount').first()
            if top and top.bidder.email:
                _send_email(
                    top.bidder,
                    f'Jūs vadāt izsolē "{title}" ar €{auction.current_price}. '
                    f'Izsole beidzas plkst. {ends} — vēl 1 stunda!',
                    url,
                )
                sent += 1

            # Pārdevējam
            seller = auction.listing.seller
            if seller.email:
                _send_email(
                    seller,
                    f'Jūsu izsole "{title}" beidzas plkst. {ends} — vēl 1 stunda! '
                    f'Pašreizējā cena: €{auction.current_price}.',
                    url,
                )
                sent += 1

        # --- Izsoles beidzas pēc 24 stundām ---
        lo, hi = _window(24)
        soon_24h = Auction.objects.filter(
            is_finished=False, ends_at__range=(lo, hi)
        ).select_related('listing__seller')

        for auction in soon_24h:
            title = auction.listing.title
            url = f'/izsoles/{auction.pk}/'
            ends = auction.ends_at.strftime('%d.%m.%Y %H:%M')

            top = auction.bids.order_by('-amount').first()
            if top and top.bidder.email:
                _send_email(
                    top.bidder,
                    f'Jūs vadāt izsolē "{title}" ar €{auction.current_price}. '
                    f'Izsole beidzas {ends} — vēl 24 stundas!',
                    url,
                )
                sent += 1

            seller = auction.listing.seller
            if seller.email:
                _send_email(
                    seller,
                    f'Jūsu izsole "{title}" beidzas {ends} — vēl 24 stundas! '
                    f'Pašreizējā cena: €{auction.current_price}.',
                    url,
                )
                sent += 1

        # --- Sludinājumi beidzas pēc 3 dienām ---
        lo, hi = _window(72)
        expiring = Listing.objects.filter(
            is_active=True,
            expires_at__range=(lo, hi),
        ).select_related('seller')

        for listing in expiring:
            if listing.seller.email:
                ends = listing.expires_at.strftime('%d.%m.%Y')
                _send_email(
                    listing.seller,
                    f'Jūsu sludinājums "{listing.title}" beidzas {ends} — vēl 3 dienas. '
                    f'Lai pagarinātu, atveriet sludinājumu.',
                    f'/sludinajumi/{listing.pk}/',
                )
                sent += 1

        self.stdout.write(self.style.SUCCESS(f'Nosūtīti {sent} atgādinājumi.'))
