from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "category", "name", "description", "price",
            "image", "featured", "is_custom", "is_accessory", "is_offer",
        )
        widgets = {
            "category": forms.Select(attrs={"class": "form-select"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Product name"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Optional description"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "featured": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_custom": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_accessory": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_offer": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # When editing, don't require a new image upload
        if self.instance and self.instance.pk:
            self.fields["image"].required = False

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise forms.ValidationError("Price must be zero or positive.")
        return price
