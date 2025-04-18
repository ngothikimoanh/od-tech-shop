from django import forms

from web.models.device import Device


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['product']
