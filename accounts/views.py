import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings

security_log = logging.getLogger('security')
from .models import Profile, EmailVerification, PhoneVerification, Wallet, WalletTransaction, AccountDeletionRequest, Notification, Rating, EmailChangeRequest
from .sms import send_sms
from decimal import Decimal, InvalidOperation

BRUTE_FORCE_LIMIT = 5
BRUTE_FORCE_TIMEOUT = 15 * 60  # 15 minūtes sekundēs


def _get_client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '127.0.0.1')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    ip = _get_client_ip(request)
    cache_key = f'login_fail_{ip}'
    fail_count = cache.get(cache_key, 0)

    if fail_count >= BRUTE_FORCE_LIMIT:
        return render(request, 'accounts/login.html', {'locked_out': True})

    unverified = False
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            cache.delete(cache_key)
            login(request, form.get_user())
            return redirect(request.GET.get('next', 'home'))
        else:
            new_count = fail_count + 1
            cache.set(cache_key, new_count, BRUTE_FORCE_TIMEOUT)
            remaining = max(0, BRUTE_FORCE_LIMIT - new_count)
            security_log.warning(f'LOGIN_FAIL ip={ip} attempt={new_count} user={request.POST.get("username","")!r}')
            if new_count >= BRUTE_FORCE_LIMIT:
                security_log.warning(f'LOCKOUT ip={ip}')

            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            try:
                user = User.objects.get(username=username)
                if not user.is_active and user.check_password(password):
                    unverified = True
            except User.DoesNotExist:
                try:
                    user = User.objects.get(email=username)
                    if not user.is_active and user.check_password(password):
                        unverified = True
                except (User.DoesNotExist, User.MultipleObjectsReturned):
                    pass

            if new_count >= BRUTE_FORCE_LIMIT:
                return render(request, 'accounts/login.html', {'locked_out': True})

            return render(request, 'accounts/login.html', {
                'form': form,
                'unverified': unverified,
                'remaining': remaining,
            })

    return render(request, 'accounts/login.html', {'form': form, 'unverified': unverified})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        email = request.POST.get('email', '').strip()
        account_type = request.POST.get('account_type', 'private')
        phone_code = request.POST.get('phone_code', '+371').strip()
        phone_number = request.POST.get('phone_number', '').strip().lstrip('0')
        phone = (phone_code + phone_number) if phone_number else ''
        errors = []

        if not email:
            errors.append('E-pasta adrese ir obligāta.')
        elif User.objects.filter(email=email).exists():
            errors.append('Šī e-pasta adrese jau tiek izmantota.')

        if not phone_number:
            errors.append('Tālruņa numurs ir obligāts.')

        country = request.POST.get('country', '').strip()
        city = request.POST.get('city', '').strip()
        if not country:
            errors.append('Valsts ir obligāta.')
        if not city:
            errors.append('Pilsēta ir obligāta.')

        if not request.POST.get('agree_terms'):
            errors.append('Jums jāpiekrīt lietošanas noteikumiem.')

        if account_type == 'private':
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            if not first_name:
                errors.append('Vārds ir obligāts.')
            if not last_name:
                errors.append('Uzvārds ir obligāts.')
        else:
            company_name = request.POST.get('company_name', '').strip()
            reg_number = request.POST.get('reg_number', '').strip()
            legal_address = request.POST.get('legal_address', '').strip()
            contact_person = request.POST.get('contact_person', '').strip()
            if not company_name:
                errors.append('Uzņēmuma nosaukums ir obligāts.')
            if not reg_number:
                errors.append('Reģistrācijas numurs ir obligāts.')
            if not legal_address:
                errors.append('Juridiskā adrese ir obligāta.')
            if not contact_person:
                errors.append('Kontaktpersona ir obligāta.')

        if form.is_valid() and not errors:
            user = form.save(commit=False)
            user.email = email
            user.is_active = False
            user.save()

            profile = Profile.objects.create(user=user, account_type=account_type)
            if account_type == 'private':
                profile.first_name = first_name
                profile.last_name = last_name
                profile.phone = phone
                profile.address = request.POST.get('address', '').strip()
            else:
                profile.company_name = company_name
                profile.reg_number = reg_number
                profile.vat_number = request.POST.get('vat_number', '').strip()
                profile.legal_address = legal_address
                profile.contact_person = contact_person
                profile.phone = phone
            profile.country = country
            profile.city = city
            profile.save()

            verification = EmailVerification.create_for_user(user)
            _send_verification_email(user, verification.token, request)

            request.session['pending_verification_email'] = email
            return redirect('verify_email_sent')

        return render(request, 'accounts/register.html', {
            'form': form, 'errors': errors, 'post': request.POST,
        })
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def _send_verification_email(user, token, request):
    link = request.build_absolute_uri(f'/accounts/verify-email/{token}/')
    subject = 'Apstipriniet savu e-pastu — eizsole.lv'
    body = (
        f'Sveiki, {user.username}!\n\n'
        f'Lai apstiprinātu savu e-pasta adresi, spiediet uz saites:\n\n'
        f'{link}\n\n'
        f'Saite derīga 24 stundas.\n\n'
        f'Ja jūs nereģistrējāties eizsole.lv, ignorējiet šo e-pastu.\n\n'
        f'— eizsole.lv komanda'
    )
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)


def verify_email_sent(request):
    email = request.session.get('pending_verification_email', '')
    return render(request, 'accounts/verify_email_sent.html', {'pending_email': email})


def verify_email(request, token):
    verification = get_object_or_404(EmailVerification, token=token)

    if not verification.is_valid():
        messages.error(request, 'Verifikācijas saite ir novecojusi vai jau izmantota.')
        return redirect('resend_verification')

    user = verification.user
    verification.is_used = True
    verification.save()

    user.is_active = True
    user.save()

    profile, _ = Profile.objects.get_or_create(user=user)
    profile.email_verified = True
    profile.save()

    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    if 'pending_verification_email' in request.session:
        del request.session['pending_verification_email']
    messages.success(request, 'E-pasts veiksmīgi apstiprināts! Laipni lūdzam!')
    return redirect('profile')


def resend_verification(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            email = request.user.email
        else:
            email = request.POST.get('email', '').strip() or request.session.get('pending_verification_email', '')

        user = User.objects.filter(email=email).first()
        if user and not user.is_active:
            verification = EmailVerification.create_for_user(user)
            _send_verification_email(user, verification.token, request)
            request.session['pending_verification_email'] = email
        elif user and user.is_active:
            profile, _ = Profile.objects.get_or_create(user=user)
            if not profile.email_verified:
                verification = EmailVerification.create_for_user(user)
                _send_verification_email(user, verification.token, request)

        messages.success(request, 'Verifikācijas e-pasts nosūtīts atkārtoti.')
        return redirect('verify_email_sent')

    email = ''
    if request.user.is_authenticated:
        email = request.user.email
    else:
        email = request.session.get('pending_verification_email', '')
    return render(request, 'accounts/resend_verification.html', {'email': email})


@login_required
def add_phone(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    error = None

    if request.method == 'POST':
        phone = request.POST.get('phone', '').strip()
        # Pamata validācija — sākas ar + un ir cipari
        clean = phone.replace(' ', '').replace('-', '')
        if not clean.startswith('+') or not clean[1:].isdigit() or len(clean) < 8:
            error = 'Ievadiet derīgu telefona numuru formātā +37126000000'
        else:
            verification = PhoneVerification.create_for_user(request.user, clean)
            send_sms(clean, f'eizsole.lv verifikācijas kods: {verification.code}')
            request.session['verify_phone'] = clean
            return redirect('verify_phone')

    return render(request, 'accounts/add_phone.html', {
        'profile': profile,
        'error': error,
        'current_phone': profile.phone,
    })


@login_required
def verify_phone(request):
    phone = request.session.get('verify_phone')
    if not phone:
        return redirect('add_phone')

    error = None

    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        verification = PhoneVerification.objects.filter(
            user=request.user, phone=phone, is_used=False
        ).first()

        if not verification or not verification.is_valid():
            error = 'Kods ir novecojis. Lūdzu pieprasiet jaunu kodu.'
        elif verification.code != code:
            error = 'Nepareizs kods. Mēģiniet vēlreiz.'
        else:
            verification.is_used = True
            verification.save()
            profile = request.user.profile
            profile.phone = phone
            profile.phone_verified = True
            profile.save()
            del request.session['verify_phone']
            messages.success(request, 'Telefona numurs veiksmīgi apstiprināts!')
            return redirect('profile')

    return render(request, 'accounts/verify_phone.html', {
        'phone': phone,
        'error': error,
    })


@login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    wallet, _ = Wallet.objects.get_or_create(user=request.user)
    from listings.models import Message
    unread_count = Message.objects.filter(recipient=request.user, is_read=False).count()

    if request.method == 'POST' and request.FILES.get('avatar'):
        avatar_file = request.FILES['avatar']
        if avatar_file.size > 5 * 1024 * 1024:
            messages.error(request, 'Attēls nedrīkst pārsniegt 5 MB.')
        elif not avatar_file.content_type.startswith('image/'):
            messages.error(request, 'Lūdzu augšupielādējiet attēlu (JPG, PNG, WEBP).')
        else:
            if profile_obj.avatar:
                profile_obj.avatar.delete(save=False)
            profile_obj.avatar = avatar_file
            profile_obj.save()
            messages.success(request, 'Avatārs atjaunināts.')
        return redirect('profile')

    from listings.models import Listing
    from django.utils import timezone
    templates = Listing.objects.filter(
        seller=request.user,
        is_template=True,
    ).order_by('-template_created_at')

    return render(request, 'accounts/profile.html', {
        'unread_count': unread_count,
        'wallet': wallet,
        'templates': templates,
    })


def public_profile(request, username):
    seller = get_object_or_404(User, username=username)
    profile_obj, _ = Profile.objects.get_or_create(user=seller)
    from listings.models import Listing
    active_listings = Listing.objects.filter(seller=seller, is_active=True, moderation_status='approved').order_by('-created_at')
    ratings = Rating.objects.filter(reviewed=seller).select_related('reviewer')
    my_rating = None
    if request.user.is_authenticated and request.user != seller:
        my_rating = Rating.objects.filter(reviewer=request.user, reviewed=seller).first()
    return render(request, 'accounts/public_profile.html', {
        'seller': seller,
        'seller_profile': profile_obj,
        'active_listings': active_listings,
        'ratings': ratings,
        'my_rating': my_rating,
    })


@login_required
def rate_user(request, username):
    from listings.models import Listing
    reviewed = get_object_or_404(User, username=username)
    if request.user == reviewed:
        messages.error(request, 'Nevar vērtēt sevi.')
        return redirect('public_profile', username=username)

    listing_pk = request.GET.get('listing') or request.POST.get('listing')
    listing = None
    if listing_pk:
        try:
            listing = Listing.objects.get(pk=listing_pk)
            # Pārbauda vai šis lietotājs drīkst novērtēt par šo darījumu
            is_seller = listing.seller == reviewed and listing.buyer == request.user
            is_buyer = listing.buyer == reviewed and listing.seller == request.user
            # Izsoles gadījums
            auction = getattr(listing, 'auction', None)
            if auction:
                is_seller = listing.seller == reviewed and auction.winner == request.user
                is_buyer = auction.winner == reviewed and listing.seller == request.user
            if not (is_seller or is_buyer):
                listing = None
        except Listing.DoesNotExist:
            listing = None

    if request.method == 'GET':
        already = Rating.objects.filter(reviewer=request.user, reviewed=reviewed, listing=listing).first()
        return render(request, 'accounts/rate_user.html', {
            'reviewed': reviewed,
            'listing': listing,
            'already': already,
        })

    if request.method == 'POST':
        stars = max(1, min(5, int(request.POST.get('stars', 5))))
        comment = request.POST.get('comment', '').strip()[:500]
        Rating.objects.update_or_create(
            reviewer=request.user, reviewed=reviewed, listing=listing,
            defaults={'stars': stars, 'comment': comment},
        )
        messages.success(request, 'Atsauksme saglabāta!')
        if listing:
            return redirect('listing_detail', pk=listing.pk)
    return redirect('public_profile', username=username)


@login_required
def notifications_view(request):
    notifs = Notification.objects.filter(user=request.user)[:50]
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return render(request, 'accounts/notifications.html', {'notifs': notifs})


@login_required
def _send_email_change_link(user, new_email, token, request):
    link = request.build_absolute_uri(f'/accounts/maina-epastu/{token}/')
    subject = 'Apstipriniet e-pasta maiņu — eizsole.lv'
    body = (
        f'Sveiki, {user.username}!\n\n'
        f'Tika pieprasīta jūsu e-pasta maiņa uz: {new_email}\n\n'
        f'Lai apstiprinātu maiņu, spiediet uz saites:\n\n'
        f'{link}\n\n'
        f'Saite derīga 24 stundas.\n\n'
        f'Ja jūs neprasījāt mainīt e-pastu, ignorējiet šo ziņu — jūsu adrese paliks nemainīta.\n\n'
        f'— eizsole.lv komanda'
    )
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)


def profile_edit(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user = request.user
        email = request.POST.get('email', '').strip()
        if email and email != user.email:
            if User.objects.filter(email=email).exclude(pk=user.pk).exists():
                messages.error(request, 'Šī e-pasta adrese jau tiek izmantota.')
                return render(request, 'accounts/profile_edit.html', {'profile': profile_obj})
            req = EmailChangeRequest.create_for_user(user, email)
            _send_email_change_link(user, email, req.token, request)
            messages.info(request, f'Apstiprinājuma saite nosūtīta uz jūsu pašreizējo e-pastu ({user.email}). Pārbaudiet iesūtni un spiediet uz saites.')
            # Pārējie lauki tiek saglabāti normāli, tikai email ne

        profile_obj.phone    = request.POST.get('phone', '').strip()
        profile_obj.country  = request.POST.get('country', '').strip()
        profile_obj.city     = request.POST.get('city', '').strip()
        profile_obj.address  = request.POST.get('address', '').strip()
        profile_obj.location = request.POST.get('location', '').strip()

        if profile_obj.account_type == 'private':
            profile_obj.first_name = request.POST.get('first_name', '').strip()
            profile_obj.last_name  = request.POST.get('last_name', '').strip()
        else:
            profile_obj.company_name    = request.POST.get('company_name', '').strip()
            profile_obj.vat_number      = request.POST.get('vat_number', '').strip()
            profile_obj.legal_address   = request.POST.get('legal_address', '').strip()
            profile_obj.contact_person  = request.POST.get('contact_person', '').strip()

        profile_obj.save()
        messages.success(request, 'Profils atjaunināts.')
        return redirect('profile')

    return render(request, 'accounts/profile_edit.html', {'profile': profile_obj})


def confirm_email_change(request, token):
    req = get_object_or_404(EmailChangeRequest, token=token)

    if not req.is_valid():
        messages.error(request, 'Saite ir nederīga vai termiņš ir beidzies.')
        return redirect('profile')

    if User.objects.filter(email=req.new_email).exclude(pk=req.user.pk).exists():
        messages.error(request, 'Šī e-pasta adrese jau tiek izmantota citā kontā.')
        req.is_used = True
        req.save()
        return redirect('profile')

    req.user.email = req.new_email
    req.user.save()
    req.is_used = True
    req.save()

    if request.user.is_authenticated and request.user == req.user:
        messages.success(request, f'E-pasta adrese veiksmīgi nomainīta uz {req.new_email}.')
    else:
        messages.success(request, f'E-pasta adrese veiksmīgi nomainīta. Piesakieties ar jauno adresi.')

    return redirect('profile')


@login_required
def request_account_deletion(request):
    if request.method == 'POST':
        profile, _ = Profile.objects.get_or_create(user=request.user)
        if not profile.phone:
            messages.error(request, 'Lai dzēstu kontu, vispirms pievienojiet tālruņa numuru profilā.')
            return redirect('profile')

        deletion = AccountDeletionRequest.create_for_user(request.user)

        # Nosūta e-pastu
        link = request.build_absolute_uri(f'/accounts/dzest-kontu/apstiprinat/{deletion.email_token}/')
        send_mail(
            'Konta dzēšanas apstiprinājums — eizsole.lv',
            f'Sveiki, {request.user.username}!\n\n'
            f'Saņēmām pieprasījumu dzēst jūsu kontu.\n\n'
            f'Lai apstiprinātu, spiediet uz saites:\n{link}\n\n'
            f'Pēc tam ievadiet SMS kodu, kas nosūtīts uz {profile.phone}.\n\n'
            f'Saite derīga 1 stundu. Ja jūs to nepieprasījāt — ignorējiet šo e-pastu.',
            settings.DEFAULT_FROM_EMAIL,
            [request.user.email],
            fail_silently=True,
        )

        # Nosūta SMS
        from .sms import send_sms
        send_sms(profile.phone, f'eizsole.lv konta dzēšanas kods: {deletion.sms_code}. Derīgs 1 stundu.')

        messages.success(request, f'Apstiprinājuma e-pasts nosūtīts uz {request.user.email}. Pārbaudiet arī tālruni.')
        return redirect('profile')
    return render(request, 'accounts/delete_account_request.html')


@login_required
def confirm_account_deletion_email(request, token):
    deletion = get_object_or_404(AccountDeletionRequest, email_token=token, user=request.user)
    if not deletion.is_valid():
        deletion.delete()
        messages.error(request, 'Apstiprinājuma saite ir beigusies. Lūdzu mēģiniet vēlreiz.')
        return redirect('profile')
    deletion.email_confirmed = True
    deletion.save()
    return render(request, 'accounts/delete_account_confirm.html', {'deletion': deletion})


@login_required
def complete_account_deletion(request, token):
    deletion = get_object_or_404(AccountDeletionRequest, email_token=token, user=request.user)
    if not deletion.is_valid() or not deletion.email_confirmed:
        messages.error(request, 'Apstiprinājums nav derīgs.')
        return redirect('profile')
    if request.method == 'POST':
        code = request.POST.get('sms_code', '').strip()
        if code != deletion.sms_code:
            messages.error(request, 'Nepareizs SMS kods.')
            return render(request, 'accounts/delete_account_confirm.html', {'deletion': deletion, 'error': True})
        from django.contrib.auth import logout
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Jūsu konts ir dzēsts.')
        return redirect('home')
    return redirect('profile')


@login_required
def wallet_view(request):
    wallet, _ = Wallet.objects.get_or_create(user=request.user)
    transactions = wallet.transactions.all()[:50]
    return render(request, 'accounts/wallet.html', {
        'wallet': wallet,
        'transactions': transactions,
    })


@login_required
def wallet_topup(request):
    wallet, _ = Wallet.objects.get_or_create(user=request.user)
    stripe_pub = getattr(settings, 'STRIPE_PUBLISHABLE_KEY', '')
    return render(request, 'accounts/wallet_topup.html', {'wallet': wallet, 'stripe_pub': stripe_pub})


@login_required
def wallet_checkout(request):
    """Izveido Stripe Checkout sesiju un novirza uz to."""
    from django.http import HttpResponseBadRequest
    try:
        amount = Decimal(request.GET.get('amount', '0')).quantize(Decimal('0.01'))
    except InvalidOperation:
        amount = Decimal('0')

    if amount < Decimal('2.00'):
        messages.error(request, 'Minimālā iemaksa ir €2.00.')
        return redirect('wallet_topup')

    import stripe as stripe_lib
    stripe_lib.api_key = settings.STRIPE_SECRET_KEY
    try:
        session = stripe_lib.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'unit_amount': int(amount * 100),
                    'product_data': {'name': f'eizsole.lv — maka papildināšana €{amount}'},
                },
                'quantity': 1,
            }],
            mode='payment',
            metadata={
                'user_id': str(request.user.pk),
                'amount': str(amount),
            },
            customer_email=request.user.email if request.user.email else None,
            success_url=request.build_absolute_uri('/accounts/maks/veiksmigs/'),
            cancel_url=request.build_absolute_uri('/accounts/maks/papildinat/'),
        )
        return redirect(session.url)
    except Exception as e:
        messages.error(request, f'Stripe kļūda: {e}')
        return redirect('wallet_topup')


@login_required
def invoice_view(request, tx_pk):
    wallet, _ = Wallet.objects.get_or_create(user=request.user)
    tx = get_object_or_404(WalletTransaction, pk=tx_pk, wallet=wallet)
    profile, _ = Profile.objects.get_or_create(user=request.user)
    amount_ex_vat = (tx.amount - tx.vat_amount).quantize(Decimal('0.01'))
    return render(request, 'accounts/invoice.html', {
        'tx': tx,
        'profile': profile,
        'amount_ex_vat': amount_ex_vat,
        'invoice_nr': f'INV-{tx.pk:06d}',
    })


@login_required
def wallet_topup_success(request):
    messages.success(request, 'Maksājums saņemts! Maks tiks papildināts dažu sekunžu laikā.')
    return redirect('wallet')


from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def stripe_webhook(request):
    import json
    stripe_secret = getattr(settings, 'STRIPE_SECRET_KEY', '')
    webhook_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', '')
    if not stripe_secret:
        return HttpResponse(status=400)

    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')

    if not webhook_secret:
        return HttpResponse(status=400)

    try:
        import stripe as stripe_lib
        stripe_lib.api_key = stripe_secret
        event = stripe_lib.Webhook.construct_event(payload, sig_header, webhook_secret)
        event_type = event.type
        session = event.data.object
    except Exception:
        return HttpResponse(status=400)

    if event_type == 'checkout.session.completed':
        try:
            payment_status = getattr(session, 'payment_status', None)
            if payment_status == 'paid':
                meta = getattr(session, 'metadata', {}) or {}
                user_id = meta['user_id']
                amount_str = meta['amount']
                stripe_id = getattr(session, 'id', '')
                if user_id and amount_str and stripe_id:
                    from django.contrib.auth.models import User
                    user = User.objects.get(pk=user_id)
                    amount = Decimal(str(amount_str)).quantize(Decimal('0.01'))
                    wallet, _ = Wallet.objects.get_or_create(user=user)
                    if not WalletTransaction.objects.filter(reference=stripe_id).exists():
                        WalletTransaction.make_deposit(wallet, amount, reference=stripe_id)
        except Exception:
            pass

    return HttpResponse(status=200)
