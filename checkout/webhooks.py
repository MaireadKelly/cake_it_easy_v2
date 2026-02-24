import logging

import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from .models import Order

logger = logging.getLogger(__name__)


@csrf_exempt
def stripe_webhook(request):
    """
    Stripe webhook handler.

    - Verifies the event using the STRIPE_WEBHOOK_SECRET.
    - Handles `payment_intent.succeeded` events.
    - Marks the matching Order (by stripe_pid) as paid.

    The Order and its line items are created in the checkout view,
    so the webhook does not create or modify orders beyond the `paid`
    flag.
    """

    secret = getattr(settings, "STRIPE_WEBHOOK_SECRET", "")
    if not secret:
        # If no secret is configured we acknowledge the webhook so
        # Stripe does not keep retrying, but no changes are made.
        logger.warning(
            "Stripe webhook received but no "
            "STRIPE_WEBHOOK_SECRET set"
        )
        return HttpResponse(status=200)

    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            secret,
        )
    except Exception:
        # Signature invalid or payload malformed
        logger.exception(
            "Stripe webhook signature verification failed"
        )
        return HttpResponseBadRequest()

    event_type = event.get("type", "")
    logger.warning(
        "Stripe webhook received: %s",
        event_type,
    )

    if event_type == "payment_intent.succeeded":
        intent = event["data"]["object"]
        pid = intent.get("id")

        logger.warning(
            "payment_intent.succeeded pid=%s",
            pid,
        )

        if not pid:
            logger.warning(
                "payment_intent.succeeded missing pid"
            )
            return HttpResponse(status=200)

        try:
            order = Order.objects.get(stripe_pid=pid)
            logger.warning(
                "Order found for pid=%s (paid=%s)",
                pid,
                order.paid,
            )

            if not order.paid:
                order.paid = True
                order.save(update_fields=["paid"])
                logger.warning(
                    "Order marked paid for pid=%s",
                    pid,
                )

        except Order.DoesNotExist:
            # If there is no matching order we simply acknowledge
            # the event. Orders are created in the checkout view.
            logger.warning(
                "No matching order found for pid=%s",
                pid,
            )

        except Exception:
            logger.exception(
                "Unexpected error handling "
                "payment_intent.succeeded"
            )

    # For all other event types we simply acknowledge receipt
    return HttpResponse(status=200)
