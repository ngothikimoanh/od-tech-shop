from django.contrib.auth import get_user_model
from django.db import models

from common.models import TimestampMixin
from orders.constants import ORDER_STATUS_CHOICES, PAYMENT_METHODS_CHOICES, OrderStatus, PaymentMethod
from products.models import Device
from users.validators import validate_phone_number

User = get_user_model()


class Order(TimestampMixin):
    buyer_phone_number = models.CharField(max_length=15, validators=[validate_phone_number])
    saler = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    payment_method = models.CharField(
        max_length=25,
        choices=PAYMENT_METHODS_CHOICES,
        default=PaymentMethod.CASH.value,
    )
    is_paid = models.BooleanField(default=False)

    address = models.CharField(max_length=255, null=True, blank=True)
    is_receive_in_store = models.BooleanField(default=True)

    status = models.CharField(
        max_length=25,
        choices=ORDER_STATUS_CHOICES,
        default=OrderStatus.PENDDING.value,
    )
    price = models.PositiveBigIntegerField()
    product_price = models.PositiveBigIntegerField(default=0)
    buyer_points = models.FloatField(default=0)

    class Meta:
        db_table = "orders"
