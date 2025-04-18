from http import HTTPMethod

from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from web.forms.order import OrderForm
from web.models.cart import Cart
from web.models.product import Product


def carts_view(request: HttpRequest):
    carts = Cart.objects.all()

    if request.user.is_authenticated:
        carts = carts.filter(user=request.user)
    else:
        browser_id = request.COOKIES.get('browser_id')
        carts = carts.filter(browser_id=browser_id)

    total_amount = sum(cart.product.price*cart.quantity for cart in carts)
    context = {
        'carts': carts,
        'count': carts.count(),
        'total_amount': total_amount
    }

    form = OrderForm(request.POST or None)
    if request.method == HTTPMethod.POST:
        is_use_point = bool(request.POST.get('isUsePoint'))
        if form.is_valid():
            form.save(total_amount=total_amount, is_use_point=is_use_point, buyer=request.user, carts=carts)
            messages.success(request, 'Đặt hàng thành công')
            return redirect('home')
        messages.error(request, 'Đặt hàng thất bại')
    context.update({'form': form})

    return render(request, 'pages/carts.html', context)


@require_POST
def carts_update_view(request: HttpRequest, product_id: int):
    action = request.POST.get('action')

    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user, product=product)
    else:
        browser_id = request.COOKIES.get('browser_id')
        cart, _ = Cart.objects.get_or_create(browser_id=browser_id, product=product)

    if action == 'plus' or action is None:
        cart.quantity += 1
        cart.save()
        if action is None:
            messages.success(request, f'Thêm <strong>{product.name}</strong> vào giỏ hàng thành công')
    else:
        cart.quantity -= 1
        if cart.quantity == 0:
            cart.delete()
        else:
            cart.save()

    previous_url = request.META.get('HTTP_REFERER', '/')
    return redirect(previous_url)
