## 1) `bag/context_processors.py` — **REPLACE/CREATE**
## 2) `bag/views.py` — **REPLACE**
## 3) `bag/urls.py` — **REPLACE/CREATE**
## 4) `bag/templates/bag/bag.html` — **REPLACE/CREATE**


## 5) `checkout/models.py` — **REPLACE**
```python
from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    full_name = models.CharField(max_length=80)
    email = models.EmailField()
    phone_number = models.CharField(max_length=32, blank=True)
    country = models.CharField(max_length=40, blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    town_or_city = models.CharField(max_length=40, blank=True)
    street_address1 = models.CharField(max_length=80, blank=True)
    street_address2 = models.CharField(max_length=80, blank=True)

    order_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stripe_pid = models.CharField(max_length=254, blank=True)
    original_bag = models.TextField(blank=True)
    paid = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    lineitem_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order_id})"
```

## 6) `checkout/forms.py` — **REPLACE/CREATE**
```python
from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'full_name', 'email', 'phone_number', 'country', 'postcode',
            'town_or_city', 'street_address1', 'street_address2'
        )
```

## 7) `checkout/views.py` — **REPLACE**
```python
import json
from decimal import Decimal

import stripe
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render, reverse

from products.models import Product
from .forms import OrderForm
from .models import Order, OrderLineItem

STRIPE_ENABLED = bool(getattr(settings, "STRIPE_PUBLIC_KEY", "") and getattr(settings, "STRIPE_SECRET_KEY", ""))
if STRIPE_ENABLED:
    stripe.api_key = settings.STRIPE_SECRET_KEY


def _calc_bag_items_and_total(request):
    bag = request.session.get('bag', {})
    items, total = [], Decimal('0.00')
    for pid, qty in bag.items():
        product = get_object_or_404(Product, pk=int(pid))
        line_total = product.price * qty
        items.append({'product': product, 'quantity': qty, 'line_total': line_total})
        total += line_total
    return items, total


def checkout(request):
    items, total = _calc_bag_items_and_total(request)
    if not items:
        messages.info(request, "Your bag is empty.")
        return redirect('product_list')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            client_secret = request.POST.get('client_secret', '')
            pid = client_secret.split('_secret')[0] if '_secret' in client_secret else ''

            order = form.save(commit=False)
            order.user = request.user if request.user.is_authenticated else None
            order.order_total = total
            order.stripe_pid = pid
            order.original_bag = json.dumps(request.session.get('bag', {}))
            order.save()

            for i in items:
                OrderLineItem.objects.create(order=order, product=i['product'], quantity=i['quantity'])

            request.session['bag'] = {}

            try:
                send_mail(
                    subject=f"Cake It Easy — Order #{order.id} confirmed",
                    message=f"Thanks for your order! Total: €{order.order_total}",
                    from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                    recipient_list=[order.email],
                    fail_silently=True,
                )
            except Exception:
                pass

            messages.success(request, f"Order placed! Reference #{order.id}")
            return redirect(reverse('checkout_success', args=[order.id]))
    else:
        form = OrderForm()

    # GET branch: create PaymentIntent if Stripe is enabled; else demo mode
    client_secret = ''
    do_stripe = STRIPE_ENABLED
    if do_stripe:
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(total * 100),
                currency=getattr(settings, 'STRIPE_CURRENCY', 'eur'),
                metadata={'integration': 'cake_it_easy_v2'},
            )
            client_secret = intent.client_secret
        except stripe.error.AuthenticationError:
            messages.error(request, "Stripe keys look invalid. Continuing without payment for now.")
            do_stripe = False
        except Exception:
            messages.error(request, "Stripe is temporarily unavailable. Continuing without payment.")
            do_stripe = False

    if not do_stripe:
        client_secret = "test_secret_disabled"
        messages.warning(request, "Stripe is not configured. Running in no-payment demo mode.")

    return render(request, 'checkout/checkout.html', {
        'form': form,
        'items': items,
        'total': total,
        'stripe_public_key': getattr(settings, "STRIPE_PUBLIC_KEY", ""),
        'client_secret': client_secret,
    })


def checkout_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'checkout/checkout_success.html', {'order': order})
```

## 8) `checkout/templates/checkout/checkout.html` — **REPLACE**
```html
{% extends 'base.html' %}
{% load static %}
{% block content %}
  <div class="container mt-5">
    <h1 class="mb-3">Checkout</h1>

    <ul class="list-unstyled">
      {% for i in items %}
        <li>{{ i.product.name }} × {{ i.quantity }} — €{{ i.line_total }}</li>
      {% endfor %}
    </ul>
    <p class="lead"><strong>Total: €{{ total }}</strong></p>

    <form id="checkout-form" method="POST" class="card card-body mt-3">
      {% csrf_token %}
      {{ form.as_p }}
      <input type="hidden" name="client_secret" id="client_secret" value="{{ client_secret }}">

      {% if stripe_public_key and client_secret and client_secret != 'test_secret_disabled' %}
        <hr>
        <h5>Card details</h5>
        <div id="card-element" class="form-control" style="padding:.6rem .75rem;"></div>
        <div id="card-errors" class="text-danger mt-2" role="alert"></div>
        <button type="submit" id="pay-btn" class="btn btn-primary mt-3">Pay €{{ total }}</button>
      {% else %}
        <button type="submit" class="btn btn-primary mt-3">Place Order</button>
        <p class="text-muted small mt-2">Payment is disabled in this environment. Your order will still be recorded for assessment.</p>
      {% endif %}
    </form>
  </div>

  {% if stripe_public_key and client_secret and client_secret != 'test_secret_disabled' %}
    <script src="https://js.stripe.com/v3/"></script>
    <script>
      (function () {
        const stripe = Stripe("{{ stripe_public_key }}");
        const clientSecret = "{{ client_secret }}";
        const elements = stripe.elements();
        const card = elements.create('card');
        card.mount('#card-element');

        const form = document.getElementById('checkout-form');
        const payBtn = document.getElementById('pay-btn');
        const errorBox = document.getElementById('card-errors');

        form.addEventListener('submit', async (e) => {
          e.preventDefault();
          if (payBtn) payBtn.disabled = true;
          errorBox.textContent = '';

          const billingDetails = {
            name: document.getElementById('id_full_name')?.value || '',
            email: document.getElementById('id_email')?.value || '',
            address: {
              line1: document.getElementById('id_street_address1')?.value || '',
              line2: document.getElementById('id_street_address2')?.value || '',
              postal_code: document.getElementById('id_postcode')?.value || '',
              city: document.getElementById('id_town_or_city')?.value || '',
              country: document.getElementById('id_country')?.value || '',
            }
          };

          const { error, paymentIntent } = await stripe.confirmCardPayment(clientSecret, {
            payment_method: { card, billing_details: billingDetails }
          });

          if (error) {
            errorBox.textContent = error.message || 'Payment failed. Please try again.';
            if (payBtn) payBtn.disabled = false;
            return;
          }
          if (paymentIntent && paymentIntent.status === 'succeeded') form.submit();
          else {
            errorBox.textContent = 'Payment not completed. Please try again.';
            if (payBtn) payBtn.disabled = false;
          }
        });
      })();
    </script>
  {% endif %}
{% endblock %}
```

## 9) `checkout/templates/checkout/checkout_success.html` — **REPLACE/CREATE**
```html
{% extends 'base.html' %}
{% block content %}
  <div class="container mt-5">
    <h1>Thanks!</h1>
    <p>Your order number is <strong>#{{ order.id }}</strong>.</p>
  </div>
{% endblock %}
```

## 10) `checkout/webhooks.py` — **CREATE**
```python
import json
import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Order

@csrf_exempt
def stripe_webhook(request):
    \"\"\"Minimal webhook to mark orders paid when Stripe confirms payment.\"\"\"
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
```

## 11) `checkout/urls.py` — **REPLACE**
```python
from django.urls import path
from . import views
from . import webhooks

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('success/<int:order_id>/', views.checkout_success, name='checkout_success'),
    path('wh/', webhooks.stripe_webhook, name='stripe_webhook'),
]
```

## 12) Project URLs — **EDIT `cake_it_easy_v2/urls.py`** (ensure these lines exist)
```python
from django.urls import include, path

urlpatterns = [
    # ... existing patterns ...
    path('bag/', include('bag.urls')),
    path('checkout/', include('checkout.urls')),
]
```

---

## Commands to run (local first, then Heroku console)
```bash
# Local
python manage.py makemigrations checkout
python manage.py migrate
python manage.py runserver

# Heroku (Dashboard → More → Run console)
python manage.py migrate
python manage.py collectstatic --noinput
```

## Stripe webhook setup (test mode)
1) Stripe Dashboard → **Developers → Webhooks → Add endpoint**.
2) URL: `https://<your-heroku-app>.herokuapp.com/checkout/wh/`.
3) Select events: **payment_intent.succeeded** (and optionally payment_intent.payment_failed).
4) After creating, click the endpoint → **Reveal signing secret** → set it as `STRIPE_WEBHOOK_SECRET` in Heroku **Config Vars**.

## Acceptance checks
- Add product → **Bag** → **Checkout** page renders with correct total.
- With test keys set: enter `4242 4242 4242 4242` → payment succeeds → order saved → redirect to success page.
- Stripe Dashboard shows the PaymentIntent; webhook marks the order **paid=True**.
- With Stripe keys unset/invalid: friendly warning; order still records (demo mode) without crash.
- Non‑staff users don’t see product CRUD controls; staff do.



---

## Bag module review — fixes & morning checklist
**Status:** URLs and views are correctly wired; context processor present; template path correct. Minimal fixes below to harden for PASS.

### 1) Harden optional legacy context (`bag/contexts.py`) — REPLACE
```python
from decimal import Decimal
from products.models import Product


def bag_contents(request):
    """
    Safe bag contents for templates (only if you explicitly use it).
    Not registered by default; 'bag.context_processors.bag_totals' is used for header count.
    """
    bag = request.session.get('bag', {})
    items = []
    total = Decimal('0.00')

    # Collect all product ids in one query
    ids = [int(pid) for pid in bag.keys()]
    products = {p.id: p for p in Product.objects.filter(id__in=ids)}

    for pid_str, qty in bag.items():
        try:
            pid = int(pid_str)
            product = products.get(pid)
            if not product:
                continue
            line_total = product.price * qty
            items.append({
                'product': product,
                'quantity': qty,
                'line_total': line_total,
            })
            total += line_total
        except Exception:
            # Skip any bad entries rather than crashing
            continue

    return {
        'bag_items': items,
        'bag_total': total,
        'bag_count': sum(bag.values()) if bag else 0,
    }
```
> Alternatively: delete `bag/contexts.py` if unused to avoid confusion.

### 2) Comment sync in `bag/views.py` (optional tidy)
Change the final comment to reflect current behavior:
```python
# For the PASS demo flow, redirect to the Bag so users can proceed to checkout
return redirect('view_bag')
```

### 3) Settings tidy (optional)
Remove the earlier env-based `EMAIL_BACKEND` so there’s only one:
- Keep: `EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"`
- Remove the earlier `EMAIL_BACKEND = os.getenv(...` line.

### Morning quick test
1) Product detail → **Add to Bag** → lands on **/bag/** with success message; header count updates.
2) **Proceed to Checkout** → totals render correctly; can place order in demo mode.
3) With Stripe keys + webhook set: card `4242 4242 4242 4242` → success → order saved → webhook flips `paid=True`.

### One last file to confirm
Please paste `templates/base.html` tomorrow so I can verify `{% load static %}`, messages block, and referenced static assets. That’s the final guardrail for avoiding production 500s.

