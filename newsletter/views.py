import os
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect
from django.urls import NoReverseMatch, reverse

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


def _safe_reverse_products() -> str:
    """
    Try several conventional names, fall back to /products/
    """
    for name in ("products", "product_list", "all_products"):
        try:
            return reverse(name)
        except NoReverseMatch:
            continue
    return "/products/"


def subscribe(request):
    """
    POST-only endpoint to create/confirm subscription and bounce back.
    Adds ?nl=1&code=... so base template can show a modal and code.
    """
    next_url = request.POST.get("next") or _safe_reverse_products()
    if request.method != "POST":
        return redirect(next_url)

    # Basic honeypot
    if request.POST.get("company"):
        messages.info(request, "Thanks!")
        return redirect(next_url)

    # Accept raw email input (no form dependency)
    email = (request.POST.get("email") or "").strip().lower()
    try:
        validate_email(email)
    except ValidationError:
        messages.error(request, "Please enter a valid email address.")
        return redirect(next_url)

    # Store subscriber (idempotent)
    NewsletterSubscriber.objects.get_or_create(email=email)

    messages.success(request, "Subscribed! Check your inbox for your 10% code.")
    code = os.getenv("NEWSLETTER_WELCOME_CODE", "WELCOME10")

    # Append flags for modal + keep optional footer anchor
    next_url = _append_query(next_url, {"nl": "1", "code": code})
    if "#newsletter" not in next_url:
        next_url += "#newsletter"

    return redirect(next_url)
