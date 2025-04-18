from enum import StrEnum
from typing import NamedTuple


class ProductType(StrEnum):
    ANDROID = 'Android'
    IPHONE = 'iPhone (IOS)'
    OTHER = 'Điện thoại phổ thông'


class Attr(NamedTuple):
    name: str


class AttrGroup(NamedTuple):
    name: str
    chilren: list[Attr]


# TODO: Update later
PRODUCT_ATTRS = [
    AttrGroup(
        'Cấu hình & Bộ nhớ',
        [
            Attr('Hệ điều hành'),
            Attr('Chip xử lý (CPU)'),
        ]
    ),
]
