from django.urls import path

from products.views import attribute, device, product

urlpatterns = [
    # List products
    path("", product.products_list_view, name="products_list"),
    path("<int:product_id>/delete", product.products_delete_view, name="products_delete"),
    path("<str:product_key>", product.product_detail_view, name="product_detail"),

    #
    # Update products
    path("<int:product_id>/update", product.products_update_view, name="products_update"),
    #
    # Attrbites
    path("<int:product_id>/attributes", attribute.product_attributes_view, name="product_attributes"),
    #
    #  Devices
    path("<int:product_id>/devices", device.product_devices_view, name="product_devices"),
]
