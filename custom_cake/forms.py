from django import forms
from django.core.exceptions import ValidationError
from .models import CustomCake


class CustomCakeForm(forms.ModelForm):
    class Meta:
        model = CustomCake
        # We set user in the view; created_on is read-only
        exclude = ("user", "created_on")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Unicorn Birthday Cake"}),
            "inscription": forms.TextInput(attrs={"class": "form-control", "placeholder": "Short message on cake"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Design notes, colors, allergies…"}),
            "occasion": forms.Select(attrs={"class": "form-control"}),
            "flavor": forms.Select(attrs={"class": "form-control"}),
            "filling": forms.Select(attrs={"class": "form-control"}),
            "size": forms.Select(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
        }
        help_texts = {
            "inscription": "Keep it short for best readability (e.g., under 30 characters).",
            "image": "Optional reference image (PNG/JPG, under 5 MB).",
        }

    def clean_inscription(self):
        text = self.cleaned_data.get("inscription", "") or ""
        if len(text) > 60:
            raise ValidationError("Please keep the inscription under 60 characters.")
        return text

    def clean_image(self):
        img = self.cleaned_data.get("image")
        if not img:
            return img
        # Lightweight size check (Cloudinary also enforces limits server-side)
        max_bytes = 5 * 1024 * 1024  # 5 MB
        if hasattr(img, "size") and img.size and img.size > max_bytes:
            raise ValidationError("Image too large (max 5 MB).")
        return img
