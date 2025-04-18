from http import HTTPMethod

from django.contrib import messages
from django.contrib.auth import login
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import redirect, render

from web.constants.user import Role
from web.decorators.user import require_login, require_not_login, require_role
from web.forms.user import LoginForm, ProfileForm, RegisterForm
from web.models.user import User


@require_not_login
def login_view(request: HttpRequest):
    form = LoginForm(request.POST or None)

    if request.method == HTTPMethod.POST:
        if form.is_valid():
            login(request=request, user=form.user)
            return render(request, "pages/redirect.html")
        messages.error(request, "Đăng nhập thất bại, vui lòng kiểm tra lại thông tin.")

    return render(request, "pages/login.html", {"form": form})


@require_not_login
def register_view(request: HttpRequest):
    form = RegisterForm(request.POST or None)

    if request.method == HTTPMethod.POST:
        if form.is_valid():
            user = form.save()
            login(request=request, user=user)
            return render(request, "pages/redirect.html")
        messages.error(request, "Đăng ký thất bại, vui lòng kiểm tra lại thông tin.")

    return render(request, "pages/register.html", {"form": form})


@require_login
def profile_view(request: HttpRequest):
    user = User.objects.get(id=request.user.id)
    form = ProfileForm(request.POST or None, instance=user)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật thông tin thành công.")
            return redirect("profile")
        messages.error(request, "Cập nhật thông tin thất bại, vui lòng kiểm tra lại thông tin.")

    return render(request, "pages/profile.html", {"form": form})


@require_role(Role.ADMIN)
def admin_users_view(request: HttpRequest):
    users = User.objects.exclude(role=Role.ADMIN)

    search_user = request.GET.get("search_user")
    if search_user:
        users = users.filter(
            Q(phone_number__contains=search_user)
            | Q(name__contains=search_user)
            | Q(email__contains=search_user)
        )

    return render(request, "pages/admin/users.html", {"users": users})
