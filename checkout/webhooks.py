import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from .models import Order


@csrf_exempt
def stripe_webhook(request):
    secret = getattr(settings, "STRIPE_WEBHOOK_SECRET", "")
    if not secret:
        return HttpResponse(status=200)

    payload = request.body
    sig = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    try:
        event = stripe.Webhook.construct_event(payload, sig, secret)
    except Exception:
        return HttpResponseBadRequest()

    if event.get("type") == "payment_intent.succeeded":
        pid = event["data"]["object"].get("id")
        try:
            order = Order.objects.get(stripe_pid=pid)
            if not order.paid:
                order.paid = True
                order.save(update_fields=["paid"])
        except Order.DoesNotExist:
            pass
    return HttpResponse(status=200)
