from decimal import Decimal, InvalidOperation
from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from .models import Auction, Bid, ProxyBid
from .proxy import process_proxy_bids, apply_proxy_for_new_proxy
from .anti_snipe import check_and_extend
from .increments import get_increment
from accounts.notifications import notify
from accounts.models import Wallet, WalletTransaction


def _validate_price(value_str, field_name='Cena'):
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


def _finish_auction(auction):
    """Pabeidz izsoli: pieraksta uzvarētāju, iekasē no maka, sūta paziņojumus."""
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
            else:
                notify(winner, 'won',
                       f'Uzvarējāt izsolē "{auction.listing.title}" par €{amount}, '
                       f'taču maka atlikums nepietiek (€{wallet.balance:.2f}). '
                       f'Lūdzu papildiniet maku!',
                       url='/accounts/maks/papildinat/')

        auction.winner = winner
        notify(auction.listing.seller, 'bid',
               f'Izsole "{auction.listing.title}" beigusies. '
               f'Uzvarētājs: {winner.username} (€{amount}).',
               url=f'/izsoles/{auction.pk}/')
    else:
        notify(auction.listing.seller, 'bid',
               f'Izsole "{auction.listing.title}" beigusies bez uzvarētāja.',
               url=f'/izsoles/{auction.pk}/')

    auction.is_finished = True
    auction.listing.is_active = False
    auction.listing.save()
    auction.save()
    ProxyBid.objects.filter(auction=auction, is_active=True).update(is_active=False)


def _root_category(cat):
    while cat.parent_id:
        cat = cat.parent
    return cat


def auction_list(request):
    from listings.models import Category
    qs = list(Auction.objects.filter(
        is_finished=False, ends_at__gt=timezone.now()
    ).select_related('listing__category__parent__parent__parent').order_by('ends_at'))

    auction_root_map = {}
    counts = {}
    for auction in qs:
        cat = auction.listing.category
        if cat:
            root = _root_category(cat)
            auction_root_map[auction.pk] = root.pk
            counts[root.pk] = counts.get(root.pk, 0) + 1

    active_pks = set(counts.keys())
    all_root_cats = Category.objects.filter(parent__isnull=True, pk__in=active_pks).order_by('order', 'pk')
    root_cats_list = [
        {'cat': c, 'count': counts.get(c.pk, 0)}
        for c in all_root_cats
    ]
    auctions = [{'obj': a, 'root_cat_pk': auction_root_map.get(a.pk, '')} for a in qs]
    return render(request, 'auctions/list.html', {
        'auctions': auctions,
        'root_cats': root_cats_list,
    })


def auction_detail(request, pk):
    auction = get_object_or_404(Auction, pk=pk)

    # Auto-pabeidz ja laiks beidzies
    if not auction.is_finished and auction.ends_at <= timezone.now():
        _finish_auction(auction)
        auction.refresh_from_db()

    bids = auction.bids.select_related('bidder').order_by('-placed_at')[:20]

    user_proxy = None
    if request.user.is_authenticated:
        user_proxy = ProxyBid.objects.filter(
            auction=auction, bidder=request.user, is_active=True
        ).first()

    return render(request, 'auctions/detail.html', {
        'auction': auction,
        'bids': bids,
        'user_proxy': user_proxy,
        'increment': get_increment(auction.current_price),
        'dutch_price': auction.dutch_current_price() if auction.auction_type == 'dutch' else None,
        'dutch_next_drop': auction.dutch_next_drop() if auction.auction_type == 'dutch' else None,
    })


def _check_seller_or_finished(request, auction, pk):
    if not auction.is_active():
        messages.error(request, 'Izsole ir beigusies.')
        return redirect('auction_detail', pk=pk)
    if request.user == auction.listing.seller:
        messages.error(request, 'Nevarat solīt savā izsolē.')
        return redirect('auction_detail', pk=pk)
    return None


@login_required
def place_bid(request, pk):
    auction = get_object_or_404(Auction, pk=pk)

    err = _check_seller_or_finished(request, auction, pk)
    if err:
        return err

    amount, amt_err = _validate_price(request.POST.get('amount', ''), 'Solījuma summa')
    if amt_err or amount is None:
        messages.error(request, amt_err or 'Solījuma summa ir obligāta.')
        return redirect('auction_detail', pk=pk)

    increment = get_increment(auction.current_price)
    min_required = auction.current_price + increment
    if amount < min_required:
        messages.error(request, f'Minimālais solījums ir €{min_required:.2f} (solis: €{increment:.0f})')
        return redirect('auction_detail', pk=pk)

    # Manuālais solījums
    Bid.objects.create(auction=auction, bidder=request.user, amount=amount, is_auto=False)
    auction.current_price = amount
    auction.save()

    # Pārbauda buy_now
    if auction.buy_now_price and amount >= auction.buy_now_price:
        auction.winner = request.user
        auction.is_finished = True
        auction.save()
        messages.success(request, f'Apsveicam! Jūs uzvarējāt izsolē par €{amount:.2f}!')
        return redirect('auction_detail', pk=pk)

    # Anti-snipe pārbaude
    extended, new_ends = check_and_extend(auction)

    # Aktivizē proxy konkurentus
    auto_fired = process_proxy_bids(auction, amount, request.user)

    if auto_fired:
        msg = (f'Jūsu solījums €{amount:.2f} pieņemts, taču automātiskais solītājs jūs pārsola. '
               f'Pašreizējā cena: €{auction.current_price:.2f}')
    else:
        reserve_msg = ' Rezerves cena sasniegta!' if auction.reserve_met() else ''
        msg = f'Jūsu solījums €{amount:.2f} pieņemts!{reserve_msg}'

    if extended:
        msg += f' ⏱ Izsole pagarināta līdz {new_ends.strftime("%H:%M:%S")} (anti-snipe).'

    if auto_fired:
        messages.warning(request, msg)
    else:
        messages.success(request, msg)

    # Paziņojums sludinājuma īpašniekam
    seller = auction.listing.seller
    if seller != request.user:
        notify(seller, 'bid',
               f'Jauns solījums €{auction.current_price:.2f} izsolē "{auction.listing.title}"',
               url=f'/izsoles/{auction.pk}/')
    # Paziņojums pārsolitajam lietotājam (gan manuāls, gan proxy)
    prev_top = Bid.objects.filter(auction=auction).exclude(bidder=request.user).order_by('-amount').first()
    if prev_top and prev_top.bidder != seller and prev_top.bidder != request.user:
        notify(prev_top.bidder, 'outbid',
               f'Jūs tikāt pārsolīts izsolē "{auction.listing.title}". Pašreizējā cena: €{auction.current_price:.2f}',
               url=f'/izsoles/{auction.pk}/')

    return redirect('auction_detail', pk=pk)


@login_required
def set_proxy_bid(request, pk):
    auction = get_object_or_404(Auction, pk=pk)

    err = _check_seller_or_finished(request, auction, pk)
    if err:
        return err

    max_amount, ma_err = _validate_price(request.POST.get('max_amount', ''), 'Maksimālā summa')
    if ma_err or max_amount is None:
        messages.error(request, ma_err or 'Maksimālā summa ir obligāta.')
        return redirect('auction_detail', pk=pk)

    increment = get_increment(auction.current_price)
    min_required = auction.current_price + increment
    if max_amount < min_required:
        messages.error(request, f'Maksimālajai summai jābūt vismaz €{min_required:.2f}')
        return redirect('auction_detail', pk=pk)

    # Deaktivē vecāku proxy šim lietotājam
    ProxyBid.objects.filter(auction=auction, bidder=request.user, is_active=True).update(is_active=False)

    proxy = ProxyBid.objects.create(
        auction=auction,
        bidder=request.user,
        max_amount=max_amount,
    )

    # Uzreiz apstrādā proxy konkurenci
    apply_proxy_for_new_proxy(auction, proxy)

    # Anti-snipe pārbaude
    extended, new_ends = check_and_extend(auction)
    if extended:
        messages.info(request, f'⏱ Izsole pagarināta līdz {new_ends.strftime("%H:%M:%S")} (anti-snipe).')

    auction.refresh_from_db()
    if auction.leading_bidder() == request.user:
        messages.success(request,
            f'Automātiskā solīšana uzstādīta! Jūs pašlaik vadāt ar €{auction.current_price:.2f}. '
            f'Sistēma automātiski solīs jūsu vietā līdz €{max_amount:.2f}.')
    else:
        messages.warning(request,
            f'Automātiskā solīšana uzstādīta (max €{max_amount:.2f}), '
            f'taču cits solītājs jūs pārsniedz. Pašreizējā cena: €{auction.current_price:.2f}.')

    return redirect('auction_detail', pk=pk)


@login_required
def cancel_proxy_bid(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    ProxyBid.objects.filter(auction=auction, bidder=request.user, is_active=True).update(is_active=False)
    messages.info(request, 'Automātiskā solīšana atcelta.')
    return redirect('auction_detail', pk=pk)


@login_required
def buy_now(request, pk):
    auction = get_object_or_404(Auction, pk=pk)

    if not auction.buy_now_price:
        messages.error(request, 'Šai izsolei nav pieejama "Pērc tūlīt" opcija.')
        return redirect('auction_detail', pk=pk)

    if not auction.is_active():
        messages.error(request, 'Izsole ir beigusies.')
        return redirect('auction_detail', pk=pk)

    if request.user == auction.listing.seller:
        messages.error(request, 'Nevarat pirkt savu izsoli.')
        return redirect('auction_detail', pk=pk)

    wallet, _ = Wallet.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if wallet.balance < auction.buy_now_price:
            messages.error(request,
                f'Nepietiek maka atlikuma. Nepieciešams: €{auction.buy_now_price:.2f}. '
                f'Jūsu atlikums: €{wallet.balance:.2f}.')
            return redirect('wallet_topup')

        WalletTransaction.make_spend(
            wallet, auction.buy_now_price,
            description=f'Pērc tūlīt: {auction.listing.title[:80]}',
            reference=f'buynow_{auction.pk}',
        )
        Bid.objects.create(auction=auction, bidder=request.user, amount=auction.buy_now_price)
        auction.current_price = auction.buy_now_price
        auction.winner = request.user
        auction.is_finished = True
        auction.save()
        auction.listing.is_active = False
        auction.listing.save()
        ProxyBid.objects.filter(auction=auction, is_active=True).update(is_active=False)

        notify(auction.listing.seller, 'bid',
               f'Jūsu izsole "{auction.listing.title}" nopirkta par €{auction.buy_now_price}! '
               f'Pircējs: {request.user.username}.',
               url=f'/izsoles/{auction.pk}/')

        messages.success(request,
            f'Pirkums veiksmīgs! Iegādājāties par €{auction.buy_now_price:.2f}. '
            f'Summa norakstīta no maka.')
        return redirect('auction_detail', pk=pk)

    return render(request, 'auctions/buy_now_confirm.html', {'auction': auction, 'wallet': wallet})


@login_required
def auction_edit(request, pk):
    auction = get_object_or_404(Auction, pk=pk, listing__seller=request.user)
    listing = auction.listing

    if auction.is_finished:
        messages.error(request, 'Pabeigtu izsoli nevar rediģēt.')
        return redirect('auction_detail', pk=pk)

    has_bids = auction.bids.exists()

    if request.method == 'POST':
        description = request.POST.get('description', '').strip()

        if not has_bids:
            new_title = request.POST.get('title', '').strip()
            if len(new_title) < 3:
                messages.error(request, 'Nosaukums ir pārāk īss — minimums 3 rakstzīmes.')
                return render(request, 'auctions/edit.html', {'auction': auction, 'listing': listing, 'has_bids': has_bids})
            if len(new_title) > 200:
                messages.error(request, 'Nosaukums ir pārāk garš — maksimums 200 rakstzīmes.')
                return render(request, 'auctions/edit.html', {'auction': auction, 'listing': listing, 'has_bids': has_bids})

            new_price, sp_err = _validate_price(request.POST.get('starting_price', ''), 'Sākumcena')
            if sp_err or new_price is None:
                messages.error(request, sp_err or 'Sākumcena ir obligāta.')
                return render(request, 'auctions/edit.html', {'auction': auction, 'listing': listing, 'has_bids': has_bids})

            listing.title = new_title
            auction.starting_price = new_price
            auction.current_price = new_price

        if len(description) > 10000:
            messages.error(request, 'Apraksts ir pārāk garš — maksimums 10 000 rakstzīmes.')
            return render(request, 'auctions/edit.html', {'auction': auction, 'listing': listing, 'has_bids': has_bids})

        listing.description = description
        listing.save()
        auction.save()
        messages.success(request, 'Izsole atjaunināta.')
        return redirect('auction_detail', pk=pk)

    return render(request, 'auctions/edit.html', {'auction': auction, 'listing': listing, 'has_bids': has_bids})


@login_required
def dutch_buy(request, pk):
    """Pircējs pieņem pašreizējo cenu Holandiešu izsolē."""
    auction = get_object_or_404(Auction, pk=pk)

    if auction.auction_type != 'dutch':
        messages.error(request, 'Šī nav Holandiešu izsole.')
        return redirect('auction_detail', pk=pk)
    if not auction.is_active():
        messages.error(request, 'Izsole ir beigusies.')
        return redirect('auction_detail', pk=pk)
    if request.user == auction.listing.seller:
        messages.error(request, 'Nevarat pirkt savu izsoli.')
        return redirect('auction_detail', pk=pk)

    price = auction.dutch_current_price()
    wallet, _ = Wallet.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if wallet.balance < price:
            messages.error(request,
                f'Nepietiek maka atlikuma. Nepieciešams: €{price:.2f}. '
                f'Jūsu atlikums: €{wallet.balance:.2f}.')
            return redirect('wallet_topup')

        WalletTransaction.make_spend(
            wallet, price,
            description=f'Holandiešu izsole: {auction.listing.title[:80]}',
            reference=f'dutch_{auction.pk}',
        )
        Bid.objects.create(auction=auction, bidder=request.user, amount=price, is_auto=False)
        auction.current_price = price
        auction.winner = request.user
        auction.is_finished = True
        auction.save()
        auction.listing.is_active = False
        auction.listing.save()

        notify(auction.listing.seller, 'bid',
               f'Jūsu Holandiešu izsole "{auction.listing.title}" pārdota par €{price:.2f}! '
               f'Pircējs: {request.user.username}.',
               url=f'/izsoles/{auction.pk}/')
        messages.success(request,
            f'Apsveicam! Iegādājāties par €{price:.2f}. Summa norakstīta no maka.')
        return redirect('auction_detail', pk=pk)

    return render(request, 'auctions/dutch_buy_confirm.html', {
        'auction': auction,
        'price': price,
        'wallet': wallet,
        'next_drop': auction.dutch_next_drop(),
    })


@login_required
def restart_auction(request, pk):
    auction = get_object_or_404(Auction, pk=pk, listing__seller=request.user)

    if not auction.is_finished or auction.winner:
        messages.error(request, 'Izsoli var atjaunot tikai ja tā beigusies bez pircēja.')
        return redirect('profile')

    if request.method == 'POST':
        ends_at_raw = request.POST.get('ends_at', '')
        try:
            ends_at_dt = parse_datetime(ends_at_raw)
            if ends_at_dt is None:
                raise ValueError
            if timezone.is_naive(ends_at_dt):
                ends_at_dt = timezone.make_aware(ends_at_dt)
            max_ends = timezone.now() + timedelta(days=30)
            min_ends = timezone.now() + timedelta(hours=1)
            if ends_at_dt > max_ends:
                ends_at_dt = max_ends
            if ends_at_dt < min_ends:
                ends_at_dt = min_ends
        except Exception:
            ends_at_dt = timezone.now() + timedelta(days=7)

        new_price = auction.starting_price
        auction.current_price = new_price
        auction.ends_at = ends_at_dt
        auction.is_finished = False
        auction.winner = None
        auction.anti_snipe_count = 0
        auction.save()
        Bid.objects.filter(auction=auction).delete()
        ProxyBid.objects.filter(auction=auction).delete()
        auction.listing.is_active = True
        auction.listing.save()
        messages.success(request, 'Izsole atjaunota.')
        return redirect('auction_detail', pk=pk)

    return render(request, 'auctions/restart.html', {'auction': auction})
