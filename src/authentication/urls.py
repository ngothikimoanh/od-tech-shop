from django.contrib.auth import views as auth_views
from django.urls import path

from authentication import views

urlpatterns = [
    path("login", views.login_view, name="auth_login"),
    path("register", views.register_view, name="auth_register"),
    path("logout", auth_views.LogoutView.as_view(next_page="home"), name="auth_logout"),
    # Google
    path("login_by_google", views.login_with_google_view, name="auth_login_by_google"),
    path("google_callback", views.google_callback_view, name="auth_google_callback"),
]
