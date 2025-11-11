# profiles/forms.py
# -------------------------------------------------------------------
# UserProfileForm:
# - Keeps Boutique Ado placeholders/autofocus and label handling.
# - Adds safe placeholder lookup (prevents KeyError on unexpected fields).
# - Includes explicit validation for phone and postcode per assessor feedback.
# -------------------------------------------------------------------

from django import forms
from .models import UserProfile
import re


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        # User is set server-side; exclude it from the form.
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated labels,
        and set autofocus on the first appropriate field.
        """
        super().__init__(*args, **kwargs)

        # Known placeholders for common Boutique Ado fields
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
            # If your model includes this, great; if not, it's harmless:
            'default_name': 'Full Name',
        }

        # Prefer autofocus on phone; else, fall back to the first field
        autofocus_field = 'default_phone_number'
        if autofocus_field in self.fields:
            self.fields[autofocus_field].widget.attrs['autofocus'] = True
        else:
            # Fallback to any first field deterministically
            first_key = next(iter(self.fields.keys()), None)
            if first_key:
                self.fields[first_key].widget.attrs['autofocus'] = True

        # Apply placeholders and classes
        for field_name, field in self.fields.items():
            if field_name != 'default_country':
                # Safe lookup to avoid KeyError for unexpected fields
                base_placeholder = placeholders.get(
                    field_name,
                    # Fallback: use label if available, else prettified field name
                    (field.label or field_name.replace('_', ' ').title())
                )
                placeholder = f'{base_placeholder} *' if field.required else base_placeholder
                field.widget.attrs['placeholder'] = placeholder

            field.widget.attrs['class'] = 'border-black rounded-0 profile-form-input'
            field.label = False

    # ---------------------------
    # VALIDATION (assessor focus)
    # ---------------------------

    def clean_default_phone_number(self):
        """
        Allow international-style numbers: optional '+' then 7–15 digits.
        Blocks alphabetic or symbol-only input per assessor feedback.
        """
        phone = self.cleaned_data.get('default_phone_number', '')
        if phone and not re.match(r'^\+?\d{7,15}$', phone):
            raise forms.ValidationError(
                "Enter a valid phone number (7–15 digits, may start with '+')."
            )
        return phone

    def clean_default_postcode(self):
        """
        Allow common postcode formats: letters/numbers/spaces/dashes, 3–10 chars.
        This comfortably covers Irish/UK styled codes while blocking symbols.
        """
        postcode = self.cleaned_data.get('default_postcode', '')
        if postcode and not re.match(r'^[A-Za-z0-9\s-]{3,10}$', postcode):
            raise forms.ValidationError(
                "Enter a valid postcode (3–10 characters, letters/numbers, space or -)."
            )
        return postcode
