import re

from django.core.exceptions import ValidationError


def validate_phone_number(phone_number: str) -> None:
    if not re.match(r"^0\d{9}$", phone_number):
        raise ValidationError("Số điện thoại này không hợp lệ.")


class CustomPasswordValidator:
    def validate(self, password, _=None):
        if not any(char.isupper() for char in password):
            raise ValidationError("Mật khẩu chứa ít nhất một chữ in hoa.")

        if not any(char.islower() for char in password):
            raise ValidationError("Mật khẩu chứa ít nhất một in thường.")

        if not any(char.isdigit() for char in password):
            raise ValidationError("Mật khẩu chứa ít nhất một số.")

        if not re.search(r"[!@#$%^&*()?]", password):
            raise ValidationError("Mật khẩu chứa ít nhất một kí tự đặc biệt (!@#$%^&*()?).")

        if " " in password:
            raise ValidationError("Mật khẩu không được chứa khoảng cách.")

    def get_help_text(self):
        return (
            "chứa ít nhất một chữ in hoa, một chữ in thường "
            "một số, một kí tự đặc biệt (!@#$%^&*()?), và không chứa khoảng trống."
        )
