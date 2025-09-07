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

# Enable Stripe only when keys are present (lets you test locally without keys)
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
            # client_secret was created on GET and embedded in the page
            client_secret = request.POST.get('client_secret', '')
            pid = client_secret.split('_secret')[0] if '_secret' in client_secret else ''

            order = form.save(commit=False)
            order.user = request.user if request.user.is_authenticated else None
            order.order_total = total
            order.stripe_pid = pid
            order.original_bag = json.dumps(request.session.get('bag', {}))
            order.save()

            for i in items:
                OrderLineItem.objects.create(
                    order=order,
                    product=i['product'],
                    quantity=i['quantity'],
                )

            # clear bag
            request.session['bag'] = {}

            # email (console backend in dev is fine)
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

    # GET branch (or POST invalid): create PaymentIntent only if Stripe is enabled.
    # If keys are invalid or Stripe is unavailable, gracefully fall back to demo mode.
    client_secret = ''
    do_stripe = STRIPE_ENABLED
    if do_stripe:
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(total * 100),
                currency=getattr(settings, "STRIPE_CURRENCY", "eur"),
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
