import os
import uuid

from django.core.validators import MinValueValidator
from django.db import models

from web.constants.product import ProductType


def product_image_path(_, filename):
    ext = filename.split(".")[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("products/", new_filename)


class Product(models.Model):
    TYPES = [(type.value, type.value) for type in ProductType]

    name = models.CharField(max_length=128)

    price = models.PositiveBigIntegerField(validators=[MinValueValidator(1)])
    brand = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=128, choices=TYPES)

    image = models.ImageField(upload_to=product_image_path, null=True, blank=True)

    def get_point(self) -> int:
        return self.price//1000

    class Meta:
        db_table = "products"
