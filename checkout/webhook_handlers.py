from django.http import HttpResponse

from .models import Order


class StripeWH_Handler:
    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        return HttpResponse(
            content=f"Unhandled event {event['type']}", status=200
        )

    def handle_payment_intent_succeeded(self, event):
        pid = event["data"]["object"]["id"]
        try:
            Order.objects.get(stripe_pid=pid)
        except Order.DoesNotExist:
            Order.objects.create(stripe_pid=pid)
        return HttpResponse(content=f"Success: {pid}", status=200)

    def handle_payment_intent_failed(self, event):
        return HttpResponse(content="Payment failed", status=200)
