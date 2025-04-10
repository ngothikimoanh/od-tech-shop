from django.urls import path

from users import views

urlpatterns = [
    path("profile", views.profile_view, name="user_profile"),
    path("auth_order", views.auth_order_view, name="auth_order"),
    path("change_password", views.change_password_view, name="user_change_password"),
    path("", views.users_list_view, name="users_list"),
    path("change-role", views.change_user_role_view, name="change_user_role"),
]
