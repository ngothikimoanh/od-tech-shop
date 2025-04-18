from django.template.defaulttags import register


@register.filter
def phone_number_mark(phone_number: str) -> str:
    return "******" + phone_number[-4:]
