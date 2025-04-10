from django.core.validators import MinValueValidator
from django.db import models

from common.models import TimestampMixin
from products.constants import DEVICE_STATUS_CHOICES, DeviceStatus
from products.helpers import format_barcode, product_image_path


class Product(TimestampMixin):
    key = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=128)
    price = models.PositiveBigIntegerField(validators=[MinValueValidator(1)])
    thumbnail_image = models.ImageField(upload_to=product_image_path, null=True, blank=True)

    class Meta:
        db_table = "products"


class Device(TimestampMixin):
    status = models.CharField(
        max_length=20,
        choices=DEVICE_STATUS_CHOICES,
        default=DeviceStatus.AVAILABLE.value,
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def get_format_id(self):
        return format_barcode(self.id)

    class Meta:
        db_table = "devices"


class AttributeGroup(TimestampMixin):
    name = models.CharField(max_length=128)

    class Meta:
        db_table = "attribute_groups"


class Attribute(TimestampMixin):
    name = models.CharField(max_length=128)
    group = models.ForeignKey(AttributeGroup, on_delete=models.CASCADE)

    class Meta:
        db_table = "attributes"


class ProductAttribute(TimestampMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "product_attributes"
