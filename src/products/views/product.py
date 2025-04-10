from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from authentication.decorators import require_login, require_role
from products.constants import DeviceStatus
from products.forms import ProductForm
from products.models import AttributeGroup, Device, Product, ProductAttribute
from users.constants import Role


@require_role(Role.ADMIN)
def products_list_view(request: HttpRequest):
    form = ProductForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Tạo sản phẩm thành công")
            return redirect("products_list")

    context = {
        "products": Product.objects.order_by("-updated_at"),
        "form": form,
    }

    return render(request, "products/list.html", context)


def product_detail_view(request: HttpRequest, product_key: str):
    product = get_object_or_404(Product, key=product_key)
    product_attributes = ProductAttribute.objects.filter(product=product)
    product_attributes = {prod_attr.attribute.id: prod_attr.value for prod_attr in product_attributes}  # type:ignore

    has_device = Device.objects.filter(product=product, status=DeviceStatus.AVAILABLE).exists()

    context = {
        "product": product,
        "attributes": AttributeGroup.objects.order_by("id"),
        "product_attributes": product_attributes,
        "has_device": has_device,
    }
    return render(request, "products/detail.html", context)


@require_role(Role.ADMIN)
def products_update_view(request: HttpRequest, product_id: int):
    product = get_object_or_404(Product, id=product_id)

    form = ProductForm(request.POST or None, request.FILES or None, instance=product)

    if request.method == "POST":
        if form.is_valid():
            product = form.save()
            messages.success(request, "Cập nhật sản phẩm thành công")
            return redirect("products_update", product_id=product.id)

    product_attributes = ProductAttribute.objects.filter(product=product)
    product_attributes = {prod_attr.attribute.id: prod_attr.value for prod_attr in product_attributes}  # type:ignore

    context = {
        "product": product,
        "form": form,
        "attributes": AttributeGroup.objects.order_by("id"),
        "product_attributes": product_attributes,
    }

    return render(request, "products/update.html", context)


@require_role(Role.ADMIN)
@require_POST
def products_delete_view(request: HttpRequest, product_id: int):
    product = get_object_or_404(Product, id=product_id)

    product.delete()
    messages.success(request, f"Xóa sản phẩm <strong>{product.name}</strong> thành công")

    return redirect("products_list")
