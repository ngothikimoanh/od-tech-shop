from django.template.defaulttags import register


@register.filter
def currency_vnd(value):
    try:
        value = float(value)
        return f"{value:,.0f}₫".replace(",", ".")
    except (ValueError, TypeError):
        return "0₫"
