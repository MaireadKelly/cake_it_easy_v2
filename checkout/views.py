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

try:
    from products.models import ProductOption
except Exception:
    ProductOption = None

from profiles.models import UserProfile
from .forms import OrderForm
from .models import Order, OrderLineItem

STRIPE_PUBLIC_KEY = getattr(settings, "STRIPE_PUBLIC_KEY", "")
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "")
STRIPE_CURRENCY = getattr(settings, "STRIPE_CURRENCY", "eur")

if STRIPE_PUBLIC_KEY and STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY


def _consume_discount_removed_notice(request):
    notice = request.session.pop("discount_removed_notice", None)
    if notice == "WELCOME10_USED":
        request.session.modified = True
        messages.warning(
            request,
            (
                "WELCOME10 has already been used on your account "
                "and has been removed from this checkout."
            ),
        )


def _pack_price(product, option):
    if option and hasattr(option, "pack_price"):
        return Decimal(option.pack_price())
    return Decimal(product.price or 0)


def _session_items(request):
    """
    Build items from session['bag'].
    When an option is present, unit_price is the **pack price** (box total).
    """
    bag = request.session.get("bag", {}) or {}
    items = []
    subtotal = Decimal("0.00")

    for key, qty in bag.items():
        try:
            parts = str(key).split("_")
            pid = int(parts[0])
            opt_id = int(parts[1]) if len(parts) == 2 else None
            quantity = int(qty)
        except (TypeError, ValueError):
            continue

        product = Product.objects.filter(pk=pid).first()
        if not product:
            continue

        option = None
        if opt_id and ProductOption:
            option = ProductOption.objects.filter(
                pk=opt_id,
                product_id=pid,
            ).first()

        unit_price = _pack_price(product, option)
        line_total = unit_price * quantity

        items.append(
            {
                "product": product,
                "option": option,
                "quantity": quantity,
                "unit_price": unit_price,
                "line_total": line_total,
                "key": key,
            }
        )

        subtotal += line_total

    return items, subtotal


@login_required
def checkout(request):
    items, subtotal = _session_items(request)
    if not items:
        messages.info(request, "Your bag is empty.")
        return redirect("product_list")

    # Show one-time message if discount was removed
    # during login/session processing
    _consume_discount_removed_notice(request)

    # Use bag context as the single source of truth (includes dynamic discount)
    bag_ctx = bag_contents(request)

    subtotal = bag_ctx.get("total", subtotal)  # pre-discount subtotal
    delivery = bag_ctx.get("delivery", Decimal("0.00"))
    discount_amount = bag_ctx.get("discount_amount") or Decimal("0.00")
    discount_code = bag_ctx.get("discount_code") or ""

    pre_discount_total = subtotal + delivery
    grand_total = pre_discount_total - discount_amount
    if grand_total < 0:
        grand_total = Decimal("0.00")

    if request.method == "POST":
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            client_secret = request.POST.get("client_secret", "")
            pid = (
                client_secret.split("_secret")[0]
                if "_secret" in client_secret
                else ""
            )

            order = order_form.save(commit=False)
            order.user = request.user
            order.stripe_pid = pid
            order.original_bag = json.dumps(
                request.session.get("bag", {})
            )

            order.order_total = pre_discount_total
            order.discount_amount = discount_amount
            order.discount_code = discount_code

            order.save()

            for item in items:
                OrderLineItem.objects.create(
                    order=order,
                    product=item["product"],
                    option=item.get("option"),
                    quantity=item["quantity"],
                    lineitem_price=item.get("unit_price"),
                )

            if request.POST.get("save_info") == "on":
                profile, _ = UserProfile.objects.get_or_create(
                    user=request.user
                )
                cd = order_form.cleaned_data

                # Save full name to User model (no migration required)
                full_name = (cd.get("full_name") or "").strip()
                if full_name:
                    parts = full_name.split()
                    request.user.first_name = parts[0]
                    request.user.last_name = (
                        " ".join(parts[1:]) if len(parts) > 1 else ""
                    )
                    request.user.save(
                        update_fields=["first_name", "last_name"]
                    )

                # Save delivery defaults to profile
                profile.default_phone_number = cd.get("phone_number")
                profile.default_country = cd.get("country")
                profile.default_postcode = cd.get("postcode")
                profile.default_town_or_city = cd.get("town_or_city")
                profile.default_street_address1 = cd.get("street_address1")
                profile.default_street_address2 = cd.get("street_address2")
                profile.save()

            request.session["bag"] = {}
            request.session.pop("discount", None)
            request.session.pop("discount_removed_notice", None)
            request.session.modified = True

            messages.success(request, "Order placed successfully.")
            return redirect("checkout_success", order_id=order.id)

        messages.error(request, "Please correct the errors in the form.")

    else:
        initial = {}

        profile = getattr(request.user, "userprofile", None) or getattr(
            request.user, "profile", None
        )

        if profile:
            full_name = (
                f"{request.user.first_name} "
                f"{request.user.last_name}"
            ).strip()

            # If username looks like an email, don't use it as "full name"
            if not full_name:
                username = (
                    (getattr(request.user, "username", "") or "").strip()
                )
                if username and "@" not in username:
                    full_name = username

            initial = {
                "full_name": full_name,
                "email": request.user.email,
                "phone_number": getattr(
                    profile, "default_phone_number", ""
                ),
                "country": getattr(profile, "default_country", ""),
                "postcode": getattr(profile, "default_postcode", ""),
                "town_or_city": getattr(
                    profile, "default_town_or_city", ""
                ),
                "street_address1": getattr(
                    profile, "default_street_address1", ""
                ),
                "street_address2": getattr(
                    profile, "default_street_address2", ""
                ),
            }

        order_form = OrderForm(initial=initial)

    client_secret = "test_secret_disabled"
    if STRIPE_PUBLIC_KEY and STRIPE_SECRET_KEY and grand_total > 0:
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(grand_total * 100),
                currency=STRIPE_CURRENCY,
                automatic_payment_methods={"enabled": True},
                metadata={
                    "bag": json.dumps(request.session.get("bag", {})),
                    "discount_code": discount_code,
                    "discount_amount": str(discount_amount),
                    "username": request.user.username,
                },
            )
            client_secret = intent.client_secret
        except Exception:
            messages.warning(request, "Stripe is not available right now.")

    context = {
        "items": items,
        "total": subtotal,
        "delivery": delivery,
        "grand_total": grand_total,
        "discount_amount": discount_amount,
        "discount_code": discount_code,
        "stripe_public_key": STRIPE_PUBLIC_KEY,
        "client_secret": client_secret,
        "order_form": order_form,
    }

    return render(request, "checkout/checkout.html", context)


@login_required
def checkout_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if not (request.user.is_staff or order.user_id == request.user.id):
        raise PermissionDenied
    return render(
        request,
        "checkout/checkout_success.html",
        {"order": order},
    )


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if not (request.user.is_staff or order.user_id == request.user.id):
        raise PermissionDenied
    return render(
        request,
        "checkout/order_detail.html",
        {"order": order},
    )


@login_required
def my_orders(request):
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
    return render(
        request,
        "checkout/my_orders.html",
        {"orders": orders},
    )
