from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from authentication.decorators import require_login, require_role
from orders.constants import ORDER_STATUS_DISPLAY, PAYMENT_METHODS_DISPLAY, OrderStatus
from orders.models import Order
from users.constants import ROLE_NOT_INCLUDE_ADMIN, Role
from users.forms import ChangePasswordForm, ProfileForm

User = get_user_model()


@require_role(Role.ADMIN)
def users_list_view(request: HttpRequest):
    users = User.objects.order_by("-is_active", "role", "first_name")

    search_user = request.GET.get("search-user", "")
    if search_user:
        users = users.filter(
            Q(phone_number__contains=search_user)
            | Q(first_name__contains=search_user)
            | Q(last_name__contains=search_user)
            | Q(email__contains=search_user)
        )

    context = {
        "users": users,
        "search_user": search_user,
        "role_display": ROLE_NOT_INCLUDE_ADMIN,
    }

    return render(request, "users/list.html", context)


@require_role(Role.ADMIN)
@require_POST
def change_user_role_view(request: HttpRequest):
    user_id = request.POST.get("user_id")
    new_role = request.POST.get("new_role")

    user = get_object_or_404(User, id=user_id)
    if new_role != Role.GUEST and not (user.first_name and user.last_name and user.email):
        messages.error(request, "Người này chưa đầy đủ <strong>Họ tên và Email</strong>")
    else:
        user.role = new_role  # type: ignore
        user.save()

    last_url = request.POST.get("lastUrl", "users_list")
    return redirect(last_url)


@require_login
def profile_view(request: HttpRequest):
    user = User.objects.get(id=request.user.id)  # type: ignore
    form = ProfileForm(request.POST or None, instance=user)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật thông tin thành công.")
            return redirect("user_profile")

        messages.error(request, "Cập nhật thông tin thất bại, vui lòng kiểm tra lại thông tin.")

    return render(request, "users/profile.html", {"form": form})


@require_login
def change_password_view(request: HttpRequest):
    form = ChangePasswordForm(request.POST or None, user=request.user)  # type: ignore

    if request.method == "POST":
        if form.is_valid():
            form.save()
            login(request, form.user)
            messages.success(request, "Đổi mật khẩu thành công")
            return render(request, "redirect_to.html", {"next": reverse("user_profile")})

    return render(request, "users/change_password.html", {"form": form})


@require_login
def auth_order_view(request: HttpRequest):
    filter_buyer_phone_number = User.objects.get(phone_number=request.user.phone_number)  # type:ignore
    orders = Order.objects.filter(buyer_phone_number=filter_buyer_phone_number)

    orders = [
        {
            "id": order.id,  # type:ignore
            "created_at": order.created_at,
            "buyer_phone_number": order.buyer_phone_number,
            "buyer": User.objects.filter(phone_number=order.buyer_phone_number).first(),
            "saler": order.saler,
            "device": order.device,
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

    return render(request, "users/auth_order.html", context)


@require_login
def user_points_view(request: HttpRequest):
    buyer = request.user
    orders = Order.objects.filter(buyer_phone_number=buyer.phone_number)  # type:ignore

    context = {
        "points": buyer.points,  # type: ignore
        "orders": orders,
    }

    return render(request, "users/profile.html", context)
