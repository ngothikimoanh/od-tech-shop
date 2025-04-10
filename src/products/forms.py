from django import forms

from products.models import Attribute, AttributeGroup, Device, Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"


class DeviceForm(forms.ModelForm):
    product = forms.CharField(required=False)
    status = forms.CharField(required=False)

    def __init__(self, product: Product, *args, **kwargs) -> None:
        self.product = product
        super().__init__(*args, **kwargs)

    def clean_product(self):
        return self.product

    class Meta:
        model = Device
        fields = "__all__"


class AttributeGroupForm(forms.ModelForm):
    class Meta:
        model = AttributeGroup
        fields = "__all__"


class AttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = "__all__"
