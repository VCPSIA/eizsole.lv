from django.urls import path
from . import views

urlpatterns = [
    path('', views.auction_list, name='auction_list'),
    path('<int:pk>/', views.auction_detail, name='auction_detail'),
    path('<int:pk>/solit/', views.place_bid, name='place_bid'),
    path('<int:pk>/proxy/', views.set_proxy_bid, name='set_proxy_bid'),
    path('<int:pk>/proxy/atcelt/', views.cancel_proxy_bid, name='cancel_proxy_bid'),
    path('<int:pk>/perc-tulīt/', views.buy_now, name='buy_now'),
    path('<int:pk>/atjaunot/', views.restart_auction, name='restart_auction'),
]
