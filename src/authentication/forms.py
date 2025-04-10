from typing import Any

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from users.validators import validate_phone_number

User = get_user_model()


class LoginForm(forms.Form):
    phone_number = forms.CharField(max_length=15, validators=[validate_phone_number])
    password = forms.CharField(max_length=128)
    user: User | None = None  # type: ignore

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")

        self.user = User.objects.filter(phone_number=phone_number).first()
        if not self.user:
            raise forms.ValidationError("Số điện thoại này chưa được đăng ký.", code="invalid")

        if not self.user.is_active:
            raise forms.ValidationError("Số điện thoại này đã bị cấm")

        return phone_number

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if not password or (self.user and not self.user.check_password(raw_password=password)):
            raise forms.ValidationError("Mật khẩu không đúng. Vui lòng kiểm tra lại", code="invalid")

        return password


class RegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=128, validators=[validate_password])
    password_confirm = forms.CharField(max_length=128, validators=[validate_password])

    def clean_password_confirm(self):
        password: str = self.cleaned_data.get("password", "")
        password_confirm: str = self.cleaned_data.get("password_confirm", "")

        if password and password != password_confirm:
            raise forms.ValidationError("Mật khẩu nhập lại không giống với mật khẩu trước")

        return password_confirm

    def save(self, commit: bool = True) -> Any:
        user_create_args = {
            "phone_number": self.cleaned_data.get("phone_number"),
            "password": self.cleaned_data.get("password"),
        }

        if not User.objects.exists():
            user = User.objects.create_superuser(**user_create_args)  # type: ignore
        else:
            user = User.objects.create_user(**user_create_args)  # type: ignore

        return user

    class Meta:
        model = User
        fields = ["phone_number", "password", "password_confirm"]
