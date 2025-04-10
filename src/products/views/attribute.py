from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from authentication.decorators import require_role
from products.forms import AttributeForm, AttributeGroupForm
from products.models import Attribute, AttributeGroup, Product, ProductAttribute
from users.constants import Role


@require_role(Role.ADMIN)
def attributes_list_view(request: HttpRequest):
    form = AttributeGroupForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            attribute_group = form.save()
            messages.success(request, f"Tạo nhóm thuộc tính <strong>{attribute_group.name}</strong> thành công")
            return redirect("attributes_list")

    context = {
        "form": form,
        "attribute_groups": AttributeGroup.objects.order_by("id"),
    }
    return render(request, "attributes/list.html", context)


@require_role(Role.ADMIN)
@require_POST
def attribute_create_view(request: HttpRequest):
    form = AttributeForm(request.POST or None)

    if form.is_valid():
        attribute = form.save()
        messages.success(request, f"Tạo thuộc tính <strong>{attribute.name}</strong> thành công")

    return redirect("attributes_list")


@require_role(Role.ADMIN)
@require_POST
def product_attributes_view(request: HttpRequest, product_id: int):
    product = get_object_or_404(Product, id=product_id)

    for attribute, value in request.POST.items():
        if attribute.startswith("attr__"):
            attribute_id = attribute[6:]
            attribute = Attribute.objects.get(id=attribute_id)

            product_attribute, _ = ProductAttribute.objects.get_or_create(
                product=product,
                attribute=attribute,
            )

            product_attribute.value = value
            product_attribute.save()

    messages.success(request, 'Cập nhật thuộc tính sản phẩm thành công')
    return redirect("products_update", product_id=product_id)


@require_role(Role.ADMIN)
@require_POST
def attribute_delete_view(request: HttpRequest, attribute_id: int):
    attribute = get_object_or_404(Attribute, id=attribute_id)

    attribute.delete()
    messages.success(request, f"Xóa thuộc tính <strong>{attribute.name}</strong> thành công")

    return redirect("attributes_list")


@require_role(Role.ADMIN)
@require_POST
def attribute_group_delete_view(request: HttpRequest, attribute_group_id: int):
    attribute_group = get_object_or_404(AttributeGroup, id=attribute_group_id)

    attribute_group.delete()
    messages.success(request, f"Xóa nhóm thuộc tính <strong>{attribute_group.name}</strong> thành công")

    return redirect("attributes_list")
