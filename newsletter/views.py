from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect, resolve_url
from django.views.decorators.http import require_POST

from .forms import NewsletterSubscriptionForm
from .models import NewsletterSubscriber


PROMO_CODE = getattr(settings, "NEWSLETTER_PROMO_CODE", "WELCOME10")


def _back_or_home(request):
    """
    Return to the referring page; fallback to the 'home' URL name if missing.
    """
    return request.META.get("HTTP_REFERER") or resolve_url("home")


def _append_nl_params(url: str, code: str) -> str:
    """
    Append newsletter success params to given URL, preserving existing query.

    Example:
        /products/?q=cake → /products/?q=cake&nl=1&code=WELCOME10
    """
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query.update({"nl": "1", "code": code})
    new_query = urlencode(query)

    return urlunsplit(
        (
            parts.scheme,
            parts.netloc,
            parts.path,
            new_query,
            parts.fragment,
        )
    )


@require_POST
def subscribe(request):
    """
    Process newsletter subscription form submission.

    - Validates email input.
    - Normalizes and re-validates email format.
    - Creates a new subscriber or shows appropriate message.
    - Redirects back to the referring page or home.
    - On first-time success, appends ?nl=1&code=... for frontend promo logic.
    """
    form = NewsletterSubscriptionForm(request.POST)

    if not form.is_valid():
        messages.error(request, "Please enter a valid email.")
        return redirect(_back_or_home(request))
    # Normalize email and source

    email = form.cleaned_data["email"].strip().lower()
    source = (form.cleaned_data.get("source") or "modal").strip()

    # Re-validate normalized email (redundant but safe)

    try:
        validate_email(email)
    except ValidationError:
        messages.error(request, "Please enter a valid email.")
        return redirect(_back_or_home(request))
    # Create new subscriber or skip if exists

    _, created = NewsletterSubscriber.objects.get_or_create(
        email=email,
        defaults={"source": source},
    )

    if created:
        messages.success(request, "Thanks! You’re subscribed.")
        target = _append_nl_params(_back_or_home(request), PROMO_CODE)
        return redirect(target)
    messages.info(request, "You're already subscribed with that email.")
    return redirect(_back_or_home(request))
