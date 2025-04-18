from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import redirect


def require_login(view_func):
    def wrapped_view(request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Bạn cần đăng nhập")
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapped_view


def require_not_login(view_func):
    def wrapped_view(request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "Bạn đã đăng nhập rồi")
            return redirect("home")
        return view_func(request, *args, **kwargs)
    return wrapped_view


def require_role(*roles):
    def inner(view_func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            if request.user.is_authenticated and request.user.role in roles:
                return view_func(request, *args, **kwargs)
            messages.warning(request, "Bạn không có quyền truy cập vào trang này")
            return redirect("home")
        return wrapper
    return inner
