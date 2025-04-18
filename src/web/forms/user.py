from typing import Any

from django import forms
from django.contrib.auth.password_validation import validate_password

from web.models import User
from web.validators.user import validate_phone_number


class LoginForm(forms.Form):
    phone_number = forms.CharField(max_length=15, validators=[validate_phone_number])
    password = forms.CharField(max_length=128)
    user: User | None = None

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")

        self.user = User.objects.filter(phone_number=phone_number).first()

        if not self.user:
            raise forms.ValidationError("Số điện thoại này chưa được đăng ký.")

        if not self.user.is_active:
            raise forms.ValidationError("Người dùng này đã bị vô hiệu hóa")

        return phone_number

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if not password:
            raise forms.ValidationError("Mật khẩu không được để trống")

        if self.user and not self.user.check_password(raw_password=password):
            raise forms.ValidationError("Mật khẩu không đúng. Vui lòng kiểm tra lại")

        return password


class RegisterForm(forms.Form):
    phone_number = forms.CharField(max_length=15, validators=[validate_phone_number])
    password = forms.CharField(max_length=128, validators=[validate_password])
    password_confirm = forms.CharField(max_length=128, validators=[validate_password])

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")

        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Số điện thoại này đã được đăng ký.")

        return phone_number

    def clean_password_confirm(self):
        password: str = self.cleaned_data.get("password", "")
        password_confirm: str = self.cleaned_data.get("password_confirm", "")

        if password and password != password_confirm:
            raise forms.ValidationError("Mật khẩu nhập lại không giống với mật khẩu trước")

        return password_confirm

    def save(self) -> Any:
        user_create_args = {
            "phone_number": self.cleaned_data.get("phone_number"),
            "password": self.cleaned_data.get("password"),
        }

        if not User.objects.exists():
            user = User.objects.create_superuser(**user_create_args)  # type: ignore
        else:
            user = User.objects.create_user(**user_create_args)  # type: ignore

        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'gender', 'birthday', 'email', 'address']
