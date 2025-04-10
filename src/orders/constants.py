from enum import StrEnum


class OrderStatus(StrEnum):
    PENDDING = "pendding"
    VERIFIED = "verified"
    SHIPPING = "shipping"
    CANCELED = "canceled"
    SUCCESS = "success"


ORDER_STATUS_DISPLAY: dict[str, str] = {
    OrderStatus.PENDDING: "Chờ xác nhận",
    OrderStatus.VERIFIED: "Đã xác nhận",
    OrderStatus.SHIPPING: "Đang giao hàng",
    OrderStatus.CANCELED: "Đã hủy",
    OrderStatus.SUCCESS: "Thành công",
}

ORDER_STATUS_CHOICES = [(status.value, status.value) for status in OrderStatus]


class PaymentMethod(StrEnum):
    CASH = "cash"
    VIET_QR = "viet-qr"


PAYMENT_METHODS_DISPLAY: dict[str, str] = {
    PaymentMethod.CASH: "Tiền mặt",
    PaymentMethod.VIET_QR: "Chuyển khoản",
}

PAYMENT_METHODS_CHOICES = [(method.value, method.value) for method in PaymentMethod]
