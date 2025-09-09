import json
import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Order

@csrf_exempt
def stripe_webhook(request):
    # "Minimal webhook to mark orders paid when Stripe confirms payment."
    webhook_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', '')
    if not webhook_secret:
        # No secret configured: acknowledge to avoid retries but do nothing
        return HttpResponse(status=200)

    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')

    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=sig_header, secret=webhook_secret
        )
    except Exception:
        return HttpResponseBadRequest()

    if event.get('type') == 'payment_intent.succeeded':
        pid = event['data']['object']['id']
        try:
            order = Order.objects.get(stripe_pid=pid)
            if not order.paid:
                order.paid = True
                order.save(update_fields=['paid'])
        except Order.DoesNotExist:
            pass  # Optional: log for reconciliation

    # You can handle other event types if desired
    return HttpResponse(status=200)