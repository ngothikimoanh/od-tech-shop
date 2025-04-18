from django.db import models

from web.models.product import Product
from web.models.user import User


class Cart(models.Model):
    browser_id = models.UUIDField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "carts"
