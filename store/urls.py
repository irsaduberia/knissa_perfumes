from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('category/<str:category>/', views.category_page, name='category_page'),
    # Fragrances
    path('fragrances/', views.fragrance_list, name='fragrance_list'),
    path('fragrances/<int:pk>/', views.fragrance_detail, name='fragrance_detail'),

    path('him/', views.him, name='him'),
path('her/', views.her, name='her'),
path('unisex/', views.unisex, name='unisex'),
path('oud/', views.oud, name='oud'),

    # Cart
    path('add-to-cart/<int:variant_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),

    path('cart/increase/<int:variant_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:variant_id>/', views.decrease_quantity, name='decrease_quantity'),

    path('remove-from-cart/<int:variant_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),

    # Checkout
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'), 

    path('place-order/', views.place_order, name='place_order'),

    path('create-admin/', views.create_admin),
]