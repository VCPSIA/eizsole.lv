from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/labot/', views.profile_edit, name='profile_edit'),
    path('pazinojumi/', views.notifications_view, name='notifications'),
    path('lietotajs/<str:username>/', views.public_profile, name='public_profile'),
    path('lietotajs/<str:username>/vertejums/', views.rate_user, name='rate_user'),

    # E-pasta verifikācija (resend PIRMS <token>, citādi Django uzskata 'resend' par tokenu)
    path('verify-email/sent/', views.verify_email_sent, name='verify_email_sent'),
    path('verify-email/resend/', views.resend_verification, name='resend_verification'),
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),

    # Telefona verifikācija
    path('add-phone/', views.add_phone, name='add_phone'),
    path('verify-phone/', views.verify_phone, name='verify_phone'),

    # Konta dzēšana
    path('dzest-kontu/', views.request_account_deletion, name='request_account_deletion'),
    path('dzest-kontu/apstiprinat/<str:token>/', views.confirm_account_deletion_email, name='confirm_account_deletion_email'),
    path('dzest-kontu/pabeigt/<str:token>/', views.complete_account_deletion, name='complete_account_deletion'),

    # Paroles atjaunošana
    path('parole/atjaunot/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        email_template_name='accounts/password_reset_email.txt',
        subject_template_name='accounts/password_reset_subject.txt',
        success_url='/accounts/parole/nosutita/',
    ), name='password_reset'),
    path('parole/nosutita/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html',
    ), name='password_reset_done'),
    path('parole/nomainit/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        success_url='/accounts/parole/nomainita/',
    ), name='password_reset_confirm'),
    path('parole/nomainita/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html',
    ), name='password_reset_complete'),

    # Maks
    path('maks/', views.wallet_view, name='wallet'),
    path('maks/papildinat/', views.wallet_topup, name='wallet_topup'),
    path('maks/checkout/', views.wallet_checkout, name='wallet_checkout'),
    path('maks/veiksmigs/', views.wallet_topup_success, name='wallet_topup_success'),
    path('maks/rekjins/<int:tx_pk>/', views.invoice_view, name='invoice'),

    # Stripe webhook
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
]
