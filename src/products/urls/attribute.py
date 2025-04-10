from django.urls import path

from products.views import attribute

urlpatterns = [
    path("", attribute.attributes_list_view, name="attributes_list"),
    path("create", attribute.attribute_create_view, name="attribute_create"),
    path("<int:attribute_id>/delete", attribute.attribute_delete_view, name="attribute_delete"),
    path("group/<int:attribute_group_id>/delete", attribute.attribute_group_delete_view, name="attribute_group_delete"),
]
