import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CustomPasswordValidator:
    def validate(self, password, user=None):

        if not any(char.isupper() for char in password):
            raise ValidationError(_("Mật khẩu chứa ít nhất một chữ in hoa."), code="password_no_upper")

        if not any(char.islower() for char in password):
            raise ValidationError(_("Mật khẩu chứa ít nhất một in thường."), code="password_no_lower")

        if not any(char.isdigit() for char in password):
            raise ValidationError(_("Mật khẩu chứa ít nhất một số."), code="password_no_digit")

        if not re.search(r"[!@#$%^&*()?]", password):
            raise ValidationError(
                _("Mật khẩu chứa ít nhất một kí tự đặc biệt (!@#$%^&*()?)."), code="password_no_special"
            )

        if " " in password:
            raise ValidationError(_("Mật khẩu không được chứa khoảng cách."), code="password_has_spaces")

    def get_help_text(self):
        return _(
            "chứa ít nhất một chữ in hoa, một chữ in thườnh "
            "một số, một kí tự đặc biệt  (!@#$%^&*()?), và không chứa khoảng trống."
        )
