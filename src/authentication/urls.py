from django.contrib.auth import views as auth_views
from django.urls import path

from authentication import views

urlpatterns = [
    path("login", views.login_view, name="auth_login"),
    path("register", views.register_view, name="auth_register"),
    path("logout", auth_views.LogoutView.as_view(next_page="home"), name="auth_logout"),

]
