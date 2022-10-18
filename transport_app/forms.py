from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Orders
from .widgets import DatePickerInput


class OrderForm(ModelForm):
    class Meta:
        model = Orders
        fields = ('name', 'phone_number', 'email', 'shipping_address', 'shipping_city',
                  'delivery_address', 'delivery_city', 'transport_type', 'datetime', 'add_info')

        labels = {
            'datetime': _('Date of shipping'),
            'add_info': _('Additional information')
        }

        widgets = {
            'datetime': DatePickerInput()
        }
