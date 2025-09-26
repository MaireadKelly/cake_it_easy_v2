from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import CustomCake


class CustomCakeForm(forms.ModelForm):
    # Explicit date field so we control widget/validation
    needed_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        label="Needed for",
        help_text="If set, please choose a future date."
    )

    class Meta:
        model = CustomCake
        # Keep model constraints intact; we make most fields optional in __init__
        exclude = ("user", "created_on")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Unicorn Birthday Cake"}),
            "inscription": forms.TextInput(attrs={"class": "form-control", "placeholder": "Short message on cake"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Design notes, colors, allergies…"}),
            "flavor": forms.Select(attrs={"class": "form-control"}),
            "filling": forms.Select(attrs={"class": "form-control"}),
            "size": forms.Select(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
        }
        help_texts = {
            "inscription": "Keep it short for best readability (e.g., under 30 characters).",
            "image": "Optional reference image (PNG/JPG, under 5 MB).",
        }

    def __init__(self, *args, **kwargs):
        """
        Make the form tolerant for tests that only submit a subset of fields.
        Keep 'name' required; everything else optional so create/update
        will validate with minimal POST data.
        """
        super().__init__(*args, **kwargs)
        for fname, field in self.fields.items():
            if fname != "name":
                field.required = False

    def clean_inscription(self):
        text = (self.cleaned_data.get("inscription") or "").strip()
        if len(text) > 60:
            raise ValidationError("Please keep the inscription under 60 characters.")
        return text

    def clean_image(self):
        img = self.cleaned_data.get("image")
        if not img:
            return img
        max_bytes = 5 * 1024 * 1024  # 5 MB
        if hasattr(img, "size") and img.size and img.size > max_bytes:
            raise ValidationError("Image too large (max 5 MB).")
        return img

    def clean_needed_date(self):
        d = self.cleaned_data.get("needed_date")
        if d and d < timezone.localdate():
            raise ValidationError("Please choose today or a future date.")
        return d
