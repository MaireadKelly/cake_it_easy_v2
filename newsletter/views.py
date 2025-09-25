import os
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

from .forms import NewsletterSignupForm
from .models import NewsletterSubscriber


def _append_query(url: str, extra: dict) -> str:
    """
    Safely append query params to any URL (preserves existing params/fragments).
    """
    parts = list(urlparse(url))
    qs = dict(parse_qsl(parts[4], keep_blank_values=True))
    qs.update(extra)
    parts[4] = urlencode(qs)
    return urlunparse(parts)

def subscribe(request):
    """
    POST-only endpoint to create/confirm subscription and bounce back.
    Adds ?nl=1&code=... so base template can show a modal.
    """
    next_url = request.POST.get("next") or reverse("product_list")
    if request.method != "POST":
        return redirect(next_url)

    form = NewsletterSignupForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data["email"].strip().lower()
        NewsletterSubscriber.objects.get_or_create(email=email)
        messages.success(request, "Thanks! You’re subscribed.")
        code = os.getenv("NEWSLETTER_WELCOME_CODE", "WELCOME10")
        # Append flags that the base template will read to open the modal.
        next_url = _append_query(next_url, {"nl": "1", "code": code})
        # Keep the anchor so the page scrolls near the footer if desired.
        if "#newsletter" not in next_url:
            next_url += "#newsletter"
        return redirect(next_url)

    messages.error(request, "Please enter a valid email address.")
    return redirect(next_url + "#newsletter")
