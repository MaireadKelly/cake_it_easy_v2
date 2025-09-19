from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    """
    Staff-facing form for creating/editing products.
    - We EXCLUDE 'sku' so the model's save() can auto-generate it.
    """
    class Meta:
        model = Product
        exclude = ('sku',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_custom': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_accessory': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_offer': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
