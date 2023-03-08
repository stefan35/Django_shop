from django.urls import path
from . import views


urlpatterns = [
    path('', views.store, name='store'),
    path('category_book/', views.categoryBook, name='category_book'),
    path('category_shirt/', views.categoryShirt, name='category_shirt'),
    path('category_watch/', views.categoryWatch, name='category_watch'),
    path('contact', views.contact, name='contact'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('login_page/', views.login_request, name='login_request'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_request, name='logout_request'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order')
]