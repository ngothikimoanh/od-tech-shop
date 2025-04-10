from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone

from users.constants import DEFAULT_FULL_NAME, ROLE_DISPLAY, Role
from users.helpers import normalize_email
from users.validators import validate_phone_number


class UserManager(BaseUserManager):
    def create_user(self, phone_number: str, password: str, **extra_fields):
        if not phone_number:
            raise ValueError("Bạn chưa nhập số điện thoại")

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)

        user.save()
        return user

    def create_superuser(self, phone_number: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("role", Role.ADMIN)

        return self.create_user(phone_number=phone_number, password=password, **extra_fields)

    def create_employeeuser(self, phone_number: str, password: str, **extra_fields):
        extra_fields.setdefault("role", Role.EMPLOYEE)

        return self.create_user(phone_number=phone_number, password=password, **extra_fields)


class RoleMixin(models.Model):
    role = models.CharField(max_length=10, default=Role.GUEST)

    class Meta:
        abstract = True

    def get_role_display(self):
        return ROLE_DISPLAY.get(self.role, "Không rõ")


class UserInfoMixin(models.Model):
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        abstract = True

    def get_full_name(self, default=DEFAULT_FULL_NAME):
        return f"{self.last_name} {self.first_name}" if self.first_name and self.last_name else default


class UserTimeMixin(models.Model):
    date_joined = models.DateTimeField(default=timezone.now)
    last_password_change = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    def get_delta_password_change(self):
        return timezone.now() - self.last_password_change


class User(AbstractBaseUser, UserInfoMixin, RoleMixin, UserTimeMixin):
    username = None

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[validate_phone_number],
        error_messages={
            "unique": "Số điện thoại này đã tồn tại.",
        },
    )

    email = models.EmailField(
        unique=True,
        blank=True,
        null=True,
        error_messages={
            "unique": "Địa chỉ email này đã tồn tại.",
        },
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    is_verify_phone_number = models.BooleanField(default=False)
    is_verify_email = models.BooleanField(default=False)

    points = models.FloatField(default=0)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    EMAIL_FIELD = "email"

    def clean(self):
        super().clean()
        if self.email:
            self.email = normalize_email(email=self.email)

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    class Meta:
        db_table = "users"
