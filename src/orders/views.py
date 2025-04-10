from http import HTTPMethod

from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from authentication.decorators import require_login, require_role
from orders.constants import ORDER_STATUS_DISPLAY, PAYMENT_METHODS_DISPLAY, OrderStatus, PaymentMethod
from orders.forms import OrderForm
from orders.models import Order
from products.constants import DeviceStatus
from products.helpers import format_barcode
from products.models import Device, Product
from users.constants import Role
from users.models import User


@require_role(Role.EMPLOYEE)
def order_create_view(request: HttpRequest):
    form = OrderForm(request.POST or None)
    action = request.POST.get('action')

    if action != 'back' and request.method == HTTPMethod.POST and form.is_valid():
        if action == 'create-order':
            order = form.save(saler=request.user)
            messages.success(request, 'Tạo đơn hàng thành công')
            if form.cleaned_data["payment_method"] == "viet-qr":
                return redirect(f"{reverse('viet_qr_code')}?order_id={order.id}&amount={order.price}")  # type:ignore
            else:
                return redirect('home')
        return render(request, 'orders/create-verify.html', {'form': form})

    return render(request, "orders/create.html", {"form": form})


def viet_qr_code_view(request: HttpRequest):
    context = {
        "amount": request.GET.get("amount", ""),
        "message": f'DH{request.GET.get("order_id", "")}',
    }

    return render(request, "orders/qr-code.html", context)


def order_success_view(request: HttpRequest):
    return render(request, "orders/success.html")


@require_role(Role.ADMIN)
def orders_list_view(request: HttpRequest):
    filter_status = request.GET.get("status") or OrderStatus.PENDDING
    orders = Order.objects.filter(status=filter_status).order_by("-updated_at")

    orders = [
        {
            "id": order.id,  # type:ignore
            "buyer_phone_number": order.buyer_phone_number,
            "buyer": User.objects.filter(phone_number=order.buyer_phone_number).first(),
            "saler": order.saler,
            "device": order.device,
            "device_id": format_barcode(order.device.id),  # type:ignore
            "product": order.device.product,
            "price": order.price,
            "payment_method": PAYMENT_METHODS_DISPLAY.get(order.payment_method, "Không rõ"),
            "status_display": ORDER_STATUS_DISPLAY.get(order.status, "Không rõ"),
            "status": order.status,
            "address": order.address,
            "is_receive_in_store": order.is_receive_in_store,
            "is_paid": order.is_paid,
        }
        for order in orders
    ]

    context = {
        "orders": orders,
    }

    return render(request, "orders/list.html", context)


@require_role(Role.ADMIN)
@require_POST
def order_verified_status_view(request: HttpRequest, order_id: int):
    order = get_object_or_404(Order, id=order_id)
    last_url = request.POST.get("last_url")

    if order.status == OrderStatus.VERIFIED:
        messages.warning(request, "Đơn hàng đã được xác nhận trước đó")
        return redirect(last_url or "orders_list")

    if order.status == OrderStatus.PENDDING:
        order.status = OrderStatus.VERIFIED
        order.save()
        messages.success(request, "Xác nhận đơn hàng thành công")
        return redirect(last_url or "orders_list")

    messages.error(request, "Đơn hàng không được phép xác nhận")

    return redirect(last_url or "orders_list")


@require_role(Role.ADMIN)
@require_POST
def order_paided_status_view(request: HttpRequest, order_id: int):
    order = get_object_or_404(Order, id=order_id)
    last_url = request.POST.get("last_url")

    if order.is_paid == True:
        messages.warning(request, "Đơn hàng đã được xác nhận thanh toán trước đó")
        return redirect(last_url or "orders_list")

    if order.status == OrderStatus.VERIFIED and not order.is_paid:
        order.is_paid = True
        order.save()
        messages.success(request, "Xác nhận thanh toán thành công")
        return redirect(last_url or "orders_list")

    messages.error(request, "Đơn hàng không được phép xác nhận thanh toán")
    return redirect(last_url or "orders_list")


@require_role(Role.ADMIN)
@require_POST
def order_shipping_status_view(request: HttpRequest, order_id: int):
    order = get_object_or_404(Order, id=order_id)
    last_url = request.POST.get("last_url")

    if order.status == OrderStatus.SHIPPING:
        messages.warning(request, "Đơn hàng đã được xác nhận giao hàng trước đó")
        return redirect(last_url or "orders_list")

    if (
        order.status == OrderStatus.VERIFIED
        and not order.is_receive_in_store
        and order.is_paid
        and order.status != "shipping"
    ):
        order.status = OrderStatus.SHIPPING
        order.save()
        messages.success(request, "Chuyển giao đơn hàng cho shipper thành công")
        return redirect(last_url or "orders_list")

    messages.error(request, "Đơn hàng không được phép chuyển giao")
    return redirect(last_url or "orders_list")


@require_role(Role.ADMIN)
@require_POST
def order_cancel_status_view(request: HttpRequest, order_id: int):
    order = get_object_or_404(Order, id=order_id)
    last_url = request.POST.get("last_url")

    if order.status == OrderStatus.CANCELED:
        messages.warning(request, "Đơn hàng đã bị hủy trước đó")
        return redirect(last_url or "orders_list")

    if order.status != OrderStatus.SUCCESS and order.status != OrderStatus.CANCELED:
        order.status = OrderStatus.CANCELED
        order.save()

        device = order.device
        device.status = DeviceStatus.AVAILABLE
        device.save()

        user = User.objects.filter(phone_number=order.buyer_phone_number).first()

        if user:
            user.points += order.buyer_points
            user.save()

        messages.success(request, "Hủy đơn hàng thành công")
        return redirect(last_url or "orders_list")

    messages.error(request, "Đơn hàng không được phép hủy")
    return redirect(last_url or "orders_list")


@require_role(Role.ADMIN)
@require_POST
def order_success_status_view(request: HttpRequest, order_id: int):
    order = get_object_or_404(Order, id=order_id)
    last_url = request.POST.get("last_url")

    if order.status == OrderStatus.SUCCESS:
        messages.warning(request, "Đơn hàng hoàn thành trước đó")
        return redirect(last_url or "orders_list")

    if (
        (order.is_receive_in_store and order.status == OrderStatus.VERIFIED and order.is_paid)
        or (not order.is_receive_in_store and order.status == OrderStatus.SHIPPING and order.is_paid)
        and order.status != OrderStatus.SUCCESS
    ):
        order.status = OrderStatus.SUCCESS
        order.save()

        buyer = User.objects.filter(phone_number=order.buyer_phone_number).first()

        if buyer:
            point_earned = order.price // 10000
            buyer.points += point_earned
            buyer.save()

        messages.success(request, "Đơn hàng đã hoàn thành")
        return redirect(last_url or "orders_list")

    messages.error(request, "Đơn hàng không thể hoàn thành")
    return redirect(last_url or "orders_list")


@require_login
def guest_order_create_view(request: HttpRequest, product_id: int):
    product = get_object_or_404(Product, id=product_id)

    device = Device.objects.filter(product=product, status=DeviceStatus.AVAILABLE.value).first()

    if not device:
        messages.error(request, "Sản phẩm hiện tại không có thiết bị khả dụng!")
        return redirect("home")

    if request.method == HTTPMethod.POST:
        address = request.POST.get("address")

        if not address:
            messages.error(request, "Vui lòng nhập địa chỉ giao hàng!")
            return redirect("guest_order_create", product_id=product_id)

        product_price = product.price

        price = product_price

        buyer_point = request.user.points

        use_points = request.POST.get("use_points")
        if use_points:
            price = product_price - buyer_point
            request.user.points = 0
            request.user.save()

        order = Order.objects.create(
            buyer_phone_number=request.user.phone_number,  # type:ignore
            device=device,
            product_price=product_price,
            price=price,
            payment_method=PaymentMethod.VIET_QR,
            address=address,
            is_receive_in_store=False,
            buyer_points=buyer_point,
        )
        device.status = DeviceStatus.ASSIGNED
        device.save()

        messages.success(request, "Đặt hàng thành công")
        return redirect(f"{reverse('viet_qr_code')}?order_id={order.id}&amount={order.price}")  # type: ignore

    context = {
        "product": product,
    }

    return render(request, "orders/guest_order.html", context)
