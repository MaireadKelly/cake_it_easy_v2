from django import forms


class NewsletterSubscriptionForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "your@email.com",
                "required": "required",
                "aria-label": "Email address",
            }
        ),
    )
    # Optional hidden field so templates (e.g., modal) can tag the origin
    source = forms.CharField(required=False, max_length=50, widget=forms.HiddenInput)
