from django.http import HttpRequest

from web.constants.product import PRODUCT_ATTRS


def get_attributes(request: HttpRequest, attributes: dict[str, str]):
    for group in PRODUCT_ATTRS:
        for attr in group.chilren:
            value = request.POST.get(attr.name)
            if value:
                attributes[attr.name] = value.strip()
