from django import forms

from web.models.cart import Cart
from web.models.order import Order, OrderProduct
from web.models.user import User


class OrderForm(forms.ModelForm):
    def save(self, total_amount: int, is_use_point: bool, buyer: User, carts: list[Cart]) -> Order:
        data = self.cleaned_data

        if is_use_point:
            point_used = buyer.points
            buyer.points = 0
            buyer.save()
        else:
            point_used = 0

        order = Order.objects.create(
            total_amount=total_amount,
            point_used=point_used,
            point=total_amount//1000,
            buyer_phone_number=data['buyer_phone_number'],
            buyer_name=data['buyer_name'],
            address=data['address'],
        )

        for cart in carts:
            OrderProduct.objects.create(
                order=order,
                product=cart.product,
                quantity=cart.quantity,
                total_amount=cart.product.price*cart.quantity,
            )
            cart.delete()

        return order

    class Meta:
        model = Order
        fields = ['buyer_phone_number', 'buyer_name', 'address']
