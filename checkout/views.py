import json
from decimal import Decimal

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from bag.context_processors import bag_contents
from products.models import Product
from profiles.models import UserProfile

from .forms import OrderForm
from .models import Order, OrderLineItem

# Stripe init
STRIPE_PUBLIC_KEY = getattr(settings, "STRIPE_PUBLIC_KEY", "")
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "")
STRIPE_CURRENCY = getattr(settings, "STRIPE_CURRENCY", "eur")
STRIPE_ENABLED = bool(STRIPE_PUBLIC_KEY and STRIPE_SECRET_KEY)
if STRIPE_ENABLED:
    stripe.api_key = STRIPE_SECRET_KEY


def _session_items(request):
    """
    Build presentational items list from session['bag'].
    Returns: (items, subtotal)
    """
    bag = request.session.get("bag", {}) or {}
    items = []
    subtotal = Decimal("0.00")

    for pid_str, qty in bag.items():
        try:
            pid = int(pid_str)
            quantity = int(qty)
        except (TypeError, ValueError):
            continue
        product = Product.objects.filter(pk=pid).first()
        if not product:
            continue
        line_total = (product.price or Decimal("0.00")) * quantity
        items.append({"product": product, "quantity": quantity, "line_total": line_total})
        subtotal += line_total

    return items, subtotal


@login_required
def checkout(request):
    """
    Checkout page:
      - shows items/totals
      - creates Stripe PaymentIntent for grand_total (subtotal + delivery)
      - on POST, saves Order + OrderLineItems
      - prefill from UserProfile (GET) and save defaults if 'save_info' (POST)
    """
    items, subtotal = _session_items(request)
    if not items:
        messages.info(request, "Your bag is empty.")
        return redirect("product_list")

    # Totals from shared context
    bag_ctx = bag_contents(request)
    total = bag_ctx.get("total", subtotal)           # subtotal
    bag_total = bag_ctx.get("bag_total", total)      # alias for templates
    delivery = bag_ctx.get("delivery", Decimal("0.00"))
    grand_total = bag_ctx.get("grand_total", total + delivery)

    if request.method == "POST":
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            # Extract PI id from client_secret
            client_secret = request.POST.get("client_secret", "")
            pid = client_secret.split("_secret")[0] if "_secret" in client_secret else ""

            order = order_form.save(commit=False)
            order.user = request.user
            order.stripe_pid = pid
            order.original_bag = json.dumps(request.session.get("bag", {}))
            order.order_total = grand_total
            order.save()

            for i in items:
                OrderLineItem.objects.create(
                    order=order, product=i["product"], quantity=i["quantity"]
                )

            # B) Save “my details” to profile if requested
            if request.POST.get("save_info") == "on":
                profile, _ = UserProfile.objects.get_or_create(user=request.user)
                cd = order_form.cleaned_data
                profile.default_phone_number = cd.get("phone_number")
                profile.default_country = cd.get("country")
                profile.default_postcode = cd.get("postcode")
                profile.default_town_or_city = cd.get("town_or_city")
                profile.default_street_address1 = cd.get("street_address1")
                profile.default_street_address2 = cd.get("street_address2")
                profile.save()

            # Clear bag
            request.session["bag"] = {}
            messages.success(request, "Order placed successfully.")
            return redirect("checkout_success", order_id=order.id)
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        # A) Prefill from existing profile
        initial = {}
        if request.user.is_authenticated:
            # handle both related_name='userprofile' and 'profile'
            profile = (getattr(request.user, 'userprofile', None)
                    or getattr(request.user, 'profile', None))
            if profile:
                initial = {
                    "full_name": (f"{request.user.first_name} {request.user.last_name}".strip()
                                or getattr(request.user, "username", "")),
                    "email": request.user.email,
                    "phone_number": getattr(profile, "default_phone_number", ""),
                    "country": getattr(profile, "default_country", ""),
                    "postcode": getattr(profile, "default_postcode", ""),
                    "town_or_city": getattr(profile, "default_town_or_city", ""),
                    "street_address1": getattr(profile, "default_street_address1", ""),
                    "street_address2": getattr(profile, "default_street_address2", ""),
                }
        order_form = OrderForm(initial=initial)


    # Create PaymentIntent for grand_totalFix
    client_secret = "test_secret_disabled"
    if STRIPE_ENABLED and grand_total > 0:
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(grand_total * 100),
                currency=STRIPE_CURRENCY,
                automatic_payment_methods={"enabled": True},
                metadata={
                    "bag": json.dumps(request.session.get("bag", {})),
                    "username": request.user.username,
                    "save_info": str(request.POST.get("save_info") == "on")
                    if request.method == "POST"
                    else "False",
                },
            )
            client_secret = intent.client_secret
        except Exception:
            messages.warning(
                request,
                "Stripe is not available right now; you can still place your order."
            )

    context = {
        "items": items,
        "total": total,
        "bag_total": bag_total,
        "delivery": delivery,
        "grand_total": grand_total,
        "stripe_public_key": STRIPE_PUBLIC_KEY,
        "client_secret": client_secret,
        "order_form": order_form,
    }
    return render(request, "checkout/checkout.html", context)


@login_required
def checkout_success(request, order_id):
    """Owner/staff-only success page with order summary."""
    order = get_object_or_404(Order, pk=order_id)
    if not (request.user.is_staff or order.user_id == request.user.id):
        raise PermissionDenied
    return render(request, "checkout/checkout_success.html", {"order": order})


@login_required
def order_detail(request, order_id):
    """
    Read-only order detail page for owner or staff.
    """
    order = get_object_or_404(Order, pk=order_id)
    if not (request.user.is_staff or order.user_id == request.user.id):
        raise PermissionDenied
    return render(request, 'checkout/order_detail.html', {'order': order})


@login_required
def my_orders(request):
    """List current user's orders (staff see all)."""
    if request.user.is_staff:
        orders = (
            Order.objects.select_related("user")
            .prefetch_related("lineitems__product")
            .order_by("-id")
        )
    else:
        orders = (
            Order.objects.filter(user=request.user)
            .select_related("user")
            .prefetch_related("lineitems__product")
            .order_by("-id")
        )
    return render(request, "checkout/my_orders.html", {"orders": orders})

