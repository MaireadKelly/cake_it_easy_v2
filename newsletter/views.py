from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
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


def _is_ajax(request) -> bool:
    """
    Detect fetch/XHR requests.
    """
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"


@require_POST
def subscribe(request):
    """
    Process newsletter subscription form submission.

    - Validates email input.
    - Normalizes and re-validates email format.
    - Creates a new subscriber or shows appropriate message.
    - Redirects back to the referring page or home.
    - On first-time success, appends ?nl=1&code=... for frontend promo logic.

    If called via fetch/AJAX, returns JSON so the modal can display the correct UI
    (new subscriber vs already subscribed).
    """
    form = NewsletterSubscriptionForm(request.POST)

    if not form.is_valid():
        msg = "Please enter a valid email."
        if _is_ajax(request):
            return JsonResponse({"created": False, "message": msg}, status=400)
        messages.error(request, msg)
        return redirect(_back_or_home(request))

    # Normalize email and source
    email = form.cleaned_data["email"].strip().lower()
    source = (form.cleaned_data.get("source") or "modal").strip()

    # Re-validate normalized email (redundant but safe)
    try:
        validate_email(email)
    except ValidationError:
        msg = "Please enter a valid email."
        if _is_ajax(request):
            return JsonResponse({"created": False, "message": msg}, status=400)
        messages.error(request, msg)
        return redirect(_back_or_home(request))

    # Create new subscriber or identify existing
    _, created = NewsletterSubscriber.objects.get_or_create(
        email=email,
        defaults={"source": source},
    )

    if created:
        success_msg = "Thanks! You’re subscribed."
        if _is_ajax(request):
            # Only return the code for first-time subscribers
            return JsonResponse(
                {
                    "created": True,
                    "message": success_msg,
                    "code": PROMO_CODE,
                },
                status=200,
            )

        messages.success(request, success_msg)
        target = _append_nl_params(_back_or_home(request), PROMO_CODE)
        return redirect(target)

    info_msg = "You're already subscribed with that email."
    if _is_ajax(request):
        return JsonResponse(
            {"created": False, "message": info_msg},
            status=200,
        )

    messages.info(request, info_msg)
    return redirect(_back_or_home(request))
