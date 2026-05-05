"""
Proxy (automātiskās) solīšanas loģika.

Algoritms:
1. Kad kāds solī manuāli vai uzstāda proxy, salīdzina ar esošajiem proxy.
2. Uzvarošais proxy automātiski pārsola par min. soli.
3. Ja abi proxy — uzvar lielākais, cena = mazākais_max + solis (vai mazākais_max, ja vienādi).
4. Solītājs neredz citu proxy maksimālo summu.
"""
from decimal import Decimal
from .models import Bid, ProxyBid
from .increments import get_increment


def process_proxy_bids(auction, incoming_amount, incoming_bidder):
    """
    Izsauc pēc katra manuāla solījuma vai jauna proxy uzstādīšanas.
    Atgriež True, ja tika veikts automātisks solījums.
    """
    step = get_increment(incoming_amount)

    # Atrod labāko aktīvo proxy, kas NAV šis solītājs
    rival_proxy = (
        ProxyBid.objects
        .filter(auction=auction, is_active=True)
        .exclude(bidder=incoming_bidder)
        .order_by('-max_amount')
        .first()
    )

    if not rival_proxy:
        return False

    # Vai konkurents var pārsolt?
    needed = Decimal(str(incoming_amount)) + step
    if rival_proxy.max_amount < needed:
        # Konkurenta proxy ir izsmelts — deaktivē
        rival_proxy.is_active = False
        rival_proxy.save()
        return False

    # Automātiskais solījums — tikai cik nepieciešams
    auto_amount = min(needed, rival_proxy.max_amount)

    Bid.objects.create(
        auction=auction,
        bidder=rival_proxy.bidder,
        amount=auto_amount,
        is_auto=True,
    )
    auction.current_price = auto_amount
    auction.save()

    # Pārbauda buy_now
    if auction.buy_now_price and auto_amount >= auction.buy_now_price:
        auction.winner = rival_proxy.bidder
        auction.is_finished = True
        auction.save()

    return True


def apply_proxy_for_new_proxy(auction, new_proxy):
    """
    Kad tiek uzstādīts jauns proxy — salīdzina ar esošo vadošo proxy.
    Noslēdz cenu starp abiem bez liekiem solījumiem.
    """
    step = auction.min_bid_increment

    existing_proxy = (
        ProxyBid.objects
        .filter(auction=auction, is_active=True)
        .exclude(bidder=new_proxy.bidder)
        .order_by('-max_amount')
        .first()
    )

    if not existing_proxy:
        # Nav konkurences — solī minimumu virs pašreizējās cenas
        step = get_increment(auction.current_price)
        needed = auction.current_price + step
        if new_proxy.max_amount >= needed:
            auto_amount = needed
        else:
            auto_amount = new_proxy.max_amount

        Bid.objects.create(
            auction=auction,
            bidder=new_proxy.bidder,
            amount=auto_amount,
            is_auto=True,
        )
        auction.current_price = auto_amount
        auction.save()
        return

    # Abu proxy konkurence
    step = get_increment(auction.current_price)
    winner_proxy = max([new_proxy, existing_proxy], key=lambda p: p.max_amount)
    loser_proxy = min([new_proxy, existing_proxy], key=lambda p: p.max_amount)

    if new_proxy.max_amount == existing_proxy.max_amount:
        # Vienādi max — uzvar tas, kurš pirmo reģistrēja (existing)
        winner_proxy = existing_proxy
        loser_proxy = new_proxy

    # Uzvarošā cena = zaudētāja max + solis (bet ne vairāk par uzvarētāja max)
    winning_amount = min(loser_proxy.max_amount + step, winner_proxy.max_amount)

    Bid.objects.create(
        auction=auction,
        bidder=winner_proxy.bidder,
        amount=winning_amount,
        is_auto=True,
    )
    auction.current_price = winning_amount
    auction.save()

    # Zaudētāja proxy deaktivē
    loser_proxy.is_active = False
    loser_proxy.save()
