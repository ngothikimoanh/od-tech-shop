from django.urls import path

from orders import views

urlpatterns = [
    path("", views.order_create_view, name="order_create"),
    path("viet_qr_code", views.viet_qr_code_view, name="viet_qr_code"),
    path("order_success", views.order_success_view, name="order_success"),
    path("list", views.orders_list_view, name="orders_list"),
    path("<int:order_id>/verified", views.order_verified_status_view, name="order_verified_status"),
    path("<int:order_id>/paided", views.order_paided_status_view, name="order_paided_status"),
    path("<int:order_id>/shipping", views.order_shipping_status_view, name="order_shipping_status"),
    path("<int:order_id>/cancel", views.order_cancel_status_view, name="order_cancel_status"),
    path("<int:order_id>/success", views.order_success_status_view, name="order_success_status"),
    # guest
    path("guest/<int:product_id>", views.guest_order_create_view, name="guest_order_create"),
]
