from django import forms

from web.models.product import Product
from web.models.product_attr import ProductAttr


class ProductForm(forms.ModelForm):
    def save(self, attributes: dict, *args, **kwargs):
        product = super().save(*args, **kwargs)

        for attr, value in attributes.items():
            ProductAttr.objects.get_or_create(
                product=product,
                name=attr,
                value=value,
            )

        return product

    class Meta:
        model = Product
        fields = ['name', 'price', 'brand', 'type', 'image']
