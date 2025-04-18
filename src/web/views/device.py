from http import HTTPMethod

from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse

from web.forms.device import DeviceForm
from web.models.device import Device
from web.models.product import Product


def admin_devices_view(request: HttpRequest):
    devices = Device.objects.all()

    product_id = request.GET.get('product_id')
    if product_id:
        devices = devices.filter(product__id=product_id)

    status = request.GET.get('status')
    if status:
        devices = devices.filter(status=status)

    form = DeviceForm(request.POST or None)
    if request.method == HTTPMethod.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'Thêm thiết bị thành công')
            return redirect(f'{reverse('admin_devices')}?product_id={product_id}')
        messages.error(request, 'Thêm thiết bị thất bại')

    products = Product.objects.all()
    context = {
        'product_id': product_id,
        'status': status,

        'products': products,
        'devices': devices
    }
    return render(request, 'pages/admin/devices.html', context)
