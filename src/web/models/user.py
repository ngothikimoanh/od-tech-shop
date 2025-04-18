from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from web.constants.user import Gender, Role
from web.validators.user import validate_phone_number


class UserManager(BaseUserManager):
    def create_user(self, phone_number: str, password: str, **extra_fields):
        if not phone_number:
            raise ValueError("Bạn chưa nhập số điện thoại")

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)

        user.save()
        return user

    def create_superuser(self, phone_number: str, password: str, **extra_fields):
        extra_fields.setdefault("role", Role.ADMIN)
        return self.create_user(phone_number=phone_number, password=password, **extra_fields)


class User(AbstractBaseUser):
    GENDERS = [(g.value, g.value) for g in Gender]

    username = None
    phone_number = models.CharField(max_length=15, unique=True, validators=[validate_phone_number])

    role = models.CharField(max_length=32, null=True, blank=True)

    name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=16, default=Gender.MALE, choices=GENDERS)
    birthday = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)

    points = models.PositiveBigIntegerField(default=0)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"

    class Meta:
        db_table = "users"
