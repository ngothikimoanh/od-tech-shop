import json

from django.db.models.functions import Lower
from django.shortcuts import render

from web.constants.product import ProductType
from web.models.product import Product
from web.utils.convert_to_int import convert_to_int


def home_view(request):
    products = Product.objects.annotate(name_lower=Lower('name'))
    brands = products.distinct('brand').values_list('brand', flat=True)

    product_search: str | None = request.GET.get("search")
    if product_search:
        products = products.filter(name_lower__contains=product_search.lower())

    product_filter = request.GET.get('filter')
    if product_filter:
        product_filter = json.loads(product_filter)
        print(f"==>> product_filter: {product_filter}")

        brands_filter = product_filter.get('brands')
        if brands_filter:
            products = products.filter(brand__in=brands_filter)

        product_types_filter = product_filter.get('productTypes')
        if product_types_filter:
            products = products.filter(type__in=product_types_filter)

        max_price_filter = convert_to_int(product_filter.get('maxPriceFilter'))
        if max_price_filter:
            products = products.filter(price__lte=max_price_filter)

    context = {
        'products': products,
        'product_types': [product_type.value for product_type in ProductType],
        'brands': brands,
    }
    return render(request, "pages/home.html", context)
