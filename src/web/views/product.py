from http import HTTPMethod

from django.contrib import messages
from django.db.models.functions import Lower
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render

from web.constants.product import PRODUCT_ATTRS
from web.constants.user import Role
from web.decorators.user import require_role
from web.forms.product import ProductForm
from web.helpers.product import get_attributes
from web.models.product import Product
from web.models.product_attr import ProductAttr


@require_role(Role.ADMIN)
def admin_products_view(request: HttpRequest):
    search_product: str | None = request.GET.get("search_product")

    products = Product.objects.annotate(name_lower=Lower('name'))
    if search_product:
        products = products.filter(name_lower__contains=search_product.lower())

    context = {
        'products': products,
    }
    return render(request, 'pages/admin/products.html', context)


@require_role(Role.ADMIN)
def admin_products_create_view(request: HttpRequest):
    form = ProductForm(request.POST or None, request.FILES or None)
    attributes: dict[str, str] = {}

    if request.method == HTTPMethod.POST:
        get_attributes(request, attributes)
        if form.is_valid():
            form.save(attributes=attributes)
            messages.success(request, 'Tạo sản phẩm thành công')
            return redirect('admin_products')
        messages.error(request, 'Tạo sản phẩm thất bại. Vui lòng kiểm tra lại')

    context = {
        'attrs': PRODUCT_ATTRS,
        'form': form,
        'attributes': attributes,
    }
    return render(request, 'pages/admin/products_create.html', context)


def products_detail_view(request: HttpRequest, product_id: int):
    product = get_object_or_404(Product, id=product_id)

    attributes = ProductAttr.objects.filter(product=product)
    attributes = {attr.name: attr.value for attr in attributes}

    context = {
        'attrs': PRODUCT_ATTRS,
        'product': product,
        'attributes': attributes,
    }
    return render(request, 'pages/products_detail.html', context)


@require_role(Role.ADMIN)
def admin_products_update_view(request: HttpRequest, product_id: int):
    product = get_object_or_404(Product, id=product_id)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)

    attributes = ProductAttr.objects.filter(product=product)
    attributes = {attr.name: attr.value for attr in attributes}

    if request.method == HTTPMethod.POST:
        get_attributes(request, attributes)
        if form.is_valid():
            form.save(attributes=attributes)
            messages.success(request, 'Cập nhật sản phẩm thành công')
            return redirect('admin_products_update', product_id=product_id)
        messages.error(request, 'Cập nhật sản phẩm thất bại. Vui lòng kiểm tra lại')

    context = {
        'attrs': PRODUCT_ATTRS,
        'form': form,
        'attributes': attributes,
    }
    return render(request, 'pages/admin/products_update.html', context)
