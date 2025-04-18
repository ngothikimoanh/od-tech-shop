from django.db import models

from web.constants.device import DeviceStatus
from web.models.product import Product


class Device(models.Model):
    STATUS = [(status.value, status.value) for status in DeviceStatus]

    status = models.CharField(max_length=20, default=DeviceStatus.AVAILABLE, choices=STATUS)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = "devices"
