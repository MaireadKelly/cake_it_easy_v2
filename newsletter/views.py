from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.conf import settings
from django.shortcuts import redirect, resolve_url
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

from .forms import NewsletterSubscriptionForm
from .models import NewsletterSubscriber


PROMO_CODE = getattr(settings, "NEWSLETTER_PROMO_CODE", "WELCOME10")


def _back_or_home(request):
    """
    Return to the page where the form was submitted; fallback to 'home' url name.
    NOTE: returning a URL string here is fine for redirect(); if HTTP_REFERER
    is empty, we pass the 'home' URL name.
    """
    return request.META.get("HTTP_REFERER") or resolve_url("home")


def _append_nl_params(url: str, code: str) -> str:
    """
    Append newsletter success params to the given URL, preserving existing query.
    Example: /products/?q=cake  ->  /products/?q=cake&nl=1&code=WELCOME10
    """
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query.update({"nl": "1", "code": code})
    new_query = urlencode(query)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, new_query, parts.fragment))


@require_POST
def subscribe(request):
    """
    Validates email, creates subscriber if new, and always redirects back to the
    referring page (or 'home'). On first-time success, adds ?nl=1&code=... so
    the frontend can reveal the promo code.
    """
    form = NewsletterSubscriptionForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Please enter a valid email.")
        return redirect(_back_or_home(request))

    # Normalize
    email = form.cleaned_data["email"].strip().lower()
    source = (form.cleaned_data.get("source") or "modal").strip() or "modal"

    # Extra defense: validate format again post-normalization
    try:
        validate_email(email)
    except ValidationError:
        messages.error(request, "Please enter a valid email.")
        return redirect(_back_or_home(request))

    # Create or noop if already exists
    _, created = NewsletterSubscriber.objects.get_or_create(
        email=email, defaults={"source": source}
    )

    if created:
        messages.success(request, "Thanks! You’re subscribed.")
        target = _append_nl_params(_back_or_home(request), PROMO_CODE)
        return redirect(target)

    messages.info(request, "You're already subscribed with that email.")
    return redirect(_back_or_home(request))
