from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.http import HttpRequest
from django.shortcuts import redirect, render
from google.auth.transport.requests import Request
from google.oauth2.id_token import verify_oauth2_token

from authentication.decorators import require_not_login
from authentication.forms import LoginForm, RegisterForm

User = get_user_model()


@require_not_login
def login_view(request: HttpRequest):
    form = LoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            login(request=request, user=form.user)
            return render(request, "redirect_to.html")

        messages.error(request, "Đăng nhập thất bại, vui lòng kiểm tra lại thông tin.")

    return render(request, "authentication/login.html", {"form": form})


@require_not_login
def register_view(request: HttpRequest):
    form = RegisterForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request=request, user=user)
            return render(request, "redirect_to.html")

        messages.error(request, "Đăng ký thất bại, vui lòng kiểm tra lại thông tin.")

    is_exist_user = User.objects.exists()

    context = {
        "form": form,
        "is_exist_user": is_exist_user,
    }

    return render(request, "authentication/register.html", context)
