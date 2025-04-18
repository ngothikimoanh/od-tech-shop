from django.contrib.auth.views import LogoutView
from django.urls import path

from web.views.cart import carts_update_view, carts_view
from web.views.device import admin_devices_view
from web.views.home import home_view
from web.views.product import (admin_products_create_view, admin_products_update_view, admin_products_view,
                               products_detail_view)
from web.views.qr import qr_view
from web.views.user import admin_users_view, login_view, profile_view, register_view

urlpatterns = [
    path('', home_view, name='home'),

    path('login', login_view, name='login'),
    path('logout', LogoutView.as_view(next_page='home'), name='logout'),

    path('register', register_view, name='register'),

    path('profile', profile_view, name='profile'),

    path('products/<int:product_id>', products_detail_view, name='products_detail'),

    path('carts', carts_view, name='carts'),
    path('carts/update/<int:product_id>', carts_update_view, name='carts_update'),
    path('qr-code/<int:amount>/<str:message>', qr_view, name='qr'),

    # Admin URL
    path('admin/users', admin_users_view, name='admin_users'),

    path('admin/products', admin_products_view, name='admin_products'),
    path('admin/products/create', admin_products_create_view, name='admin_products_create'),
    path('admin/products/<int:product_id>/update', admin_products_update_view, name='admin_products_update'),

    path('admin/devices', admin_devices_view, name='admin_devices'),
]
