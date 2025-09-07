from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'category', 'sku', 'name', 'description', 'price',
            'image', 'featured', 'is_custom', 'is_accessory', 'is_offer'
        )
