from django import forms

from .models import Order

# Common ISO 3166-1 alpha-2 codes you expect to ship to.
COUNTRY_CHOICES = [
    ("", "Choose…"),
    ("IE", "Ireland"),
    ("GB", "United Kingdom"),
    ("US", "United States"),
    ("FR", "France"),
    ("DE", "Germany"),
    # add more as you need
]

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            "full_name", "email", "phone_number",
            "country", "postcode", "town_or_city",
            "street_address1", "street_address2",
        )
        # Default widgets; we'll add classes in __init__ below
        widgets = {
            # Text inputs
            "full_name": forms.TextInput(),
            "email": forms.EmailInput(),
            "phone_number": forms.TextInput(),
            "street_address1": forms.TextInput(),
            "street_address2": forms.TextInput(),
            "town_or_city": forms.TextInput(),
            "postcode": forms.TextInput(),
            # Use a Select for country to ensure ISO codes
            "country": forms.Select(choices=COUNTRY_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes consistently
        for name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, (forms.TextInput, forms.EmailInput, forms.NumberInput)):
                existing = widget.attrs.get("class", "")
                widget.attrs["class"] = (existing + " form-control").strip()
            elif isinstance(widget, forms.Select):
                existing = widget.attrs.get("class", "")
                widget.attrs["class"] = (existing + " form-select").strip()

        # Friendly placeholders (optional)
        self.fields["full_name"].widget.attrs.setdefault("placeholder", "Full name")
        self.fields["email"].widget.attrs.setdefault("placeholder", "name@example.com")
        self.fields["phone_number"].widget.attrs.setdefault("placeholder", "08x…")
        self.fields["street_address1"].widget.attrs.setdefault("placeholder", "Address line 1")
        self.fields["street_address2"].widget.attrs.setdefault("placeholder", "Address line 2 (optional)")
        self.fields["town_or_city"].widget.attrs.setdefault("placeholder", "Town / City")
        self.fields["postcode"].widget.attrs.setdefault("placeholder", "Eircode / Postcode")

        # Make some fields required (align with your model/UX)
        for req in ("full_name", "email", "street_address1", "town_or_city", "country"):
            self.fields[req].required = True

    def clean_country(self):
        """
        Ensure we store an uppercase 2-letter ISO code (e.g. 'IE').
        Works even if a template or alternate widget sneaks in lowercase values.
        """
        val = (self.cleaned_data.get("country") or "").strip().upper()
        # Allow empty only if field not required
        if val and len(val) != 2:
            raise forms.ValidationError("Please select a valid 2-letter country code.")
        return val
