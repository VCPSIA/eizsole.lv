from django.urls import path
from . import views

urlpatterns = [
    path('',             views.blog_list,   name='blog_list'),
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),
]

static_urlpatterns = [
    path('privatuma-politika/', views.static_page, {'page_type': 'privacy'}, name='privacy_policy'),
    path('lietosanas-noteikumi/', views.static_page, {'page_type': 'terms'},  name='terms_of_use'),
    path('jautajumi/',           views.static_page, {'page_type': 'faq'},    name='faq'),
]
