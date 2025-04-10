from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone

from users.constants import Role

User = get_user_model()


class ProfileForm(forms.ModelForm):
    def clean_email(self):
        email = self.cleaned_data.get("email")

        if self.instance.role != Role.GUEST and not email:
            raise forms.ValidationError("Email không được để trống")

        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")

        if self.instance.role != Role.GUEST and not first_name:
            raise forms.ValidationError("Tên không được để trống")

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")

        if self.instance.role != Role.GUEST and not last_name:
            raise forms.ValidationError("Họ không được để trống")

        return last_name

    class Meta:
        model = User
        fields = ["phone_number", "email", "first_name", "last_name"]


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField()
    new_password = forms.CharField(max_length=128, validators=[validate_password])
    new_password_again = forms.CharField(max_length=128, validators=[validate_password])

    user: User  # type: ignore

    def __init__(self, *args, user: User, **kwargs):  # type: ignore
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_old_password(self):
        old_password: str = self.cleaned_data.get("old_password", "")

        if not self.user.check_password(old_password):
            raise forms.ValidationError("Mật khẩu cũ nhập không chính xác")

        return old_password

    def clean_new_password(self):
        old_password: str = self.cleaned_data.get("old_password", "")
        new_password: str = self.cleaned_data.get("new_password", "")

        if old_password == new_password:
            raise forms.ValidationError("Mật khẩu mới của bạn trùng với mật khẩu cũ")

        return new_password

    def clean_new_password_again(self):
        new_password: str = self.cleaned_data.get("new_password", "")
        new_password_again: str = self.cleaned_data.get("new_password_again", "")

        if new_password and new_password_again != new_password:
            raise forms.ValidationError("Mật khẩu nhập lại không giống với mật khẩu trước")

        return new_password_again

    def save(self):
        new_password: str = self.cleaned_data.get("new_password", "")
        self.user.set_password(new_password)
        self.user.last_password_change = timezone.now()
        self.user.save()
