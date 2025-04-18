from django.db import models
from django.utils import timezone

from web.models.product import Product
from web.validators.user import validate_phone_number


class Order(models.Model):
    time_order = models.DateTimeField(default=timezone.now)
    time_delivered = models.DateTimeField(null=True, blank=True)
    time_shipping = models.DateTimeField(null=True, blank=True)

    total_amount = models.PositiveBigIntegerField()
    total_amount_transfer = models.PositiveBigIntegerField(default=0)
    total_amount_cash = models.PositiveBigIntegerField(default=0)

    buyer_phone_number = models.CharField(max_length=15, validators=[validate_phone_number])
    buyer_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    point_used = models.PositiveBigIntegerField()
    point = models.PositiveBigIntegerField()

    class Meta:
        db_table = "orders"


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveSmallIntegerField()
    total_amount = models.PositiveBigIntegerField()

    class Meta:
        db_table = "order_products"
