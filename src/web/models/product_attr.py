from django.db import models

from web.models.product import Product


class ProductAttr(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    value = models.TextField()

    class Meta:
        db_table = "product_attrs"
