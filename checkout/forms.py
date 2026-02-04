from django import forms
from .models import Order

# Common ISO 3166-1 alpha-2 codes

COUNTRY_CHOICES = [
    ("", "Choose…"),
    ("IE", "Ireland"),
    ("GB", "United Kingdom"),
    ("US", "United States"),
    ("FR", "France"),
    ("DE", "Germany"),
    # Add more as needed
]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            "full_name",
            "email",
            "phone_number",
            "country",
            "postcode",
            "town_or_city",
            "street_address1",
            "street_address2",
        )
        widgets = {
            "full_name": forms.TextInput(),
            "email": forms.EmailInput(),
            "phone_number": forms.TextInput(),
            "street_address1": forms.TextInput(),
            "street_address2": forms.TextInput(),
            "town_or_city": forms.TextInput(),
            "postcode": forms.TextInput(),
            "country": forms.Select(choices=COUNTRY_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes

        for field in self.fields.values():
            widget = field.widget
            existing_class = widget.attrs.get("class", "")
            if isinstance(
                widget, (forms.TextInput, forms.EmailInput, forms.NumberInput)
            ):
                widget.attrs["class"] = (
                    f"{existing_class} form-control".strip()
                )
            elif isinstance(widget, forms.Select):
                widget.attrs["class"] = f"{existing_class} form-select".strip()
        # Placeholders
        self.fields["country"].widget.attrs.pop(
            "maxlength", None)

        self.fields["full_name"].widget.attrs.setdefault(
            "placeholder", "Full name"
        )
        self.fields["email"].widget.attrs.setdefault(
            "placeholder", "name@example.com"
        )
        self.fields["phone_number"].widget.attrs.setdefault(
            "placeholder", "08x…"
        )
        self.fields["street_address1"].widget.attrs.setdefault(
            "placeholder", "Address line 1"
        )
        self.fields["street_address2"].widget.attrs.setdefault(
            "placeholder", "Address line 2 (optional)"
        )
        self.fields["town_or_city"].widget.attrs.setdefault(
            "placeholder", "Town / City"
        )
        self.fields["postcode"].widget.attrs.setdefault(
            "placeholder", "Eircode / Postcode"
        )

        # Required fields

        required_fields = [
            "full_name",
            "email",
            "street_address1",
            "town_or_city",
            "country",
        ]
        for field_name in required_fields:
            self.fields[field_name].required = True

    def clean_country(self):
        """
        Normalize and validate the country code (2-letter ISO format).
        """
        val = (self.cleaned_data.get("country") or "").strip().upper()
        if val and len(val) != 2:
            raise forms.ValidationError(
                "Please select a valid 2-letter country code."
            )
        return val
