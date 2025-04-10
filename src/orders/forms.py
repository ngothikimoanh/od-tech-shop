from django import forms

from orders.constants import PAYMENT_METHODS_CHOICES
from orders.models import Order
from products.constants import DEVICE_STATUS_DISPLAY, DeviceStatus
from products.helpers import decode_device_id
from products.models import Device
from users.models import User
from users.validators import validate_phone_number


class OrderForm(forms.Form):
    buyer_phone_number = forms.CharField(max_length=15, validators=[validate_phone_number])
    buyer: User | None = None

    device_id = forms.CharField()
    device: Device | None = None

    is_receive_in_store = forms.BooleanField(required=False)

    address = forms.CharField(max_length=255, required=False)

    payment_method = forms.ChoiceField(choices=PAYMENT_METHODS_CHOICES)

    is_use_point = forms.BooleanField(required=False)

    def clean_buyer_phone_number(self):
        buyer_phone_number = self.cleaned_data.get('buyer_phone_number')
        self.buyer = User.objects.filter(phone_number=buyer_phone_number).first()
        return buyer_phone_number

    def clean_device_id(self):
        device_id = self.cleaned_data.get("device_id", "")
        device_id = decode_device_id(barcode=device_id)

        self.device = Device.objects.filter(id=device_id).first()

        if not self.device:
            raise forms.ValidationError("Thiết bị không tồn tại")

        if self.device.status != DeviceStatus.AVAILABLE:
            raise forms.ValidationError(
                f'Tình trạng thiết bị: {DEVICE_STATUS_DISPLAY.get(self.device.status, "Không rõ")}'
            )

        return device_id

    def clean_address(self):
        is_receive_in_store = self.cleaned_data.get("is_receive_in_store")
        address = self.cleaned_data.get("address")

        if not is_receive_in_store and not address:
            raise forms.ValidationError("Nếu không nhận hàng ở cửa hàng. Vui lòng cung cấp địa chỉ giao hàng")

        return address

    def save(self, saler: User):
        data = self.cleaned_data

        product_price = self.device.product.price
        buyer_point = 0

        self.device.status = DeviceStatus.ASSIGNED
        self.device.save()

        if self.buyer and data['is_use_point']:
            buyer_point = self.buyer.points
            self.buyer.points = 0
            self.buyer.save()

        return Order.objects.create(
            buyer_phone_number=data['buyer_phone_number'],
            saler=saler,
            device=self.device,
            payment_method=data['payment_method'],
            address=data['address'],
            is_receive_in_store=data['is_receive_in_store'],
            price=product_price-buyer_point if data['is_use_point'] else product_price,
            product_price=product_price,
            buyer_points=buyer_point,
        )
