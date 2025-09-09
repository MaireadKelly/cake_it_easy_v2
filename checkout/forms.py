from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'full_name','email','phone_number','country','postcode',
            'town_or_city','street_address1','street_address2',
        )
        widgets = {k: forms.TextInput(attrs={'class': 'form-control'})
                   for k in ('full_name','phone_number','country','postcode',
                             'town_or_city','street_address1','street_address2')}
        widgets['email'] = forms.EmailInput(attrs={'class': 'form-control'})