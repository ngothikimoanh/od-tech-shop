from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render

from authentication.decorators import require_role
from products.constants import DEVICE_STATUS_DISPLAY
from products.forms import DeviceForm
from products.helpers import format_barcode
from products.models import Device, Product
from users.constants import Role


@require_role(Role.ADMIN)
def product_devices_view(request: HttpRequest, product_id: int):
    product = get_object_or_404(Product, id=product_id)

    devices = Device.objects.filter(product=product).order_by("-updated_at")
    devices = [
        {
            "id": format_barcode(device.id),  # type: ignore
            "status_display": DEVICE_STATUS_DISPLAY.get(device.status, "Không rõ"),
        }
        for device in devices
    ]

    form = DeviceForm(data=request.POST or None, product=product)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Thiết bị đã được đăng ký")
            return redirect("product_devices", product_id=product.id)  # type: ignore

    context = {
        "form": form,
        "product": product,
        "devices": devices,
    }

    return render(request, "devices/list.html", context)
