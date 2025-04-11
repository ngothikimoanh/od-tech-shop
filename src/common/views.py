from products.models import Product
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.shortcuts import redirect, render

User = get_user_model()


def home_view(request):
    if not User.objects.exists():
        return redirect("auth_register")

    products = (
        Product.objects.annotate(device_count=Count("device", filter=Q(device__status="available")))
        .exclude(device_count=0)
        .order_by("-device_count")
    )
    sort_option = request.GET.get("sortOption", "").strip()

    if sort_option == "price_asc":
        products = products.order_by("price")
    elif sort_option == "price_desc":
        products = products.order_by("-price")
    elif sort_option == "name_asc":
        products = products.order_by("name")
    elif sort_option == "name_desc":
        products = products.order_by("-name")

    brand_mapping = {
        'S': 'Samsung',
        'I': 'iPhone',
        'O': 'Oppo',
        'X': 'Xiaomi',
        "V": 'Vivo',
        "H": 'Hornor',
    }

    for product in products:
        first_letter = product.name[0].upper()
        product.brand = brand_mapping.get(first_letter, 'Khác')

    selected_brand = request.GET.get('brand', '').strip()
    if selected_brand and selected_brand != "all":
        products = [p for p in products if p.brand == selected_brand]

    search = request.GET.get("search", "").strip()
    if search:
        products = products.filter(
            Q(key__contains=search) | Q(name__contains=search) | Q(price__contains=search),
        )
        if not products.exists():  # Nếu không tìm thấy sản phẩm nào
            return render(request, "not_found.html")

    context = {
        "products": products,
        "search": search,
        "sort_option": sort_option,
        "selected_brand": selected_brand,
    }
    return render(request, "home.html", context)
