from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'default_phone_number',
            'default_country',
            'default_postcode',
            'default_town_or_city',
            'default_street_address1',
            'default_street_address2',
        )
        widgets = {
            'default_phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'default_country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'default_postcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postcode'}),
            'default_town_or_city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Town/City'}),
            'default_street_address1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street address 1'}),
            'default_street_address2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street address 2'}),
        }
