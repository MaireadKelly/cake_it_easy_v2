import json
from decimal import Decimal

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render, reverse

from products.models import Product
from .forms import OrderForm
from .models import Order, OrderLineItem

# --- Stripe enablement guard (keeps local running even without keys) ---
STRIPE_ENABLED = bool(
    getattr(settings, "STRIPE_PUBLIC_KEY", "") and getattr(settings, "STRIPE_SECRET_KEY", "")
)
if STRIPE_ENABLED:
    stripe.api_key = settings.STRIPE_SECRET_KEY


def _calc_bag_items_and_total(request):
    """
    Reads the current session 'bag' and returns (items, total).
    items: [{'product': Product, 'quantity': int, 'line_total': Decimal}, ...]
    """
    bag = request.session.get('bag', {})
    items, total = [], Decimal('0.00')
    for pid, qty in bag.items():
        product = get_object_or_404(Product, pk=int(pid))
        line_total = product.price * qty
        items.append({'product': product, 'quantity': qty, 'line_total': line_total})
        total += line_total
    return items, total


def _get_user_profile(user):
    """
    Safely get either user.userprofile (Boutique Ado style)
    or user.profile (your alternative). Returns None if absent.
    """
    return getattr(user, 'userprofile', getattr(user, 'profile', None))


@login_required
def checkout(request):
    """
    - GET: render OrderForm (prefilled from profile if available) and create a PaymentIntent.
    - POST: validate OrderForm, save Order + OrderLineItems, optionally persist defaults to profile,
            then redirect to checkout_success.
    """
    items, total = _calc_bag_items_and_total(request)
    if not items:
        messages.info(request, "Your bag is empty.")
        # Adjust this url name if your list view differs
        return redirect('product_list')

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            # Pull Stripe PaymentIntent id (pid) from hidden client_secret input
            client_secret = request.POST.get('client_secret', '')
            pid = client_secret.split('_secret')[0] if '_secret' in client_secret else ''

            # Create the Order but don't commit yet
            order = order_form.save(commit=False)
            order.user = request.user
            order.order_total = total
            order.stripe_pid = pid
            order.original_bag = json.dumps(request.session.get('bag', {}))
            order.save()

            # Create line items
            for i in items:
                OrderLineItem.objects.create(
                    order=order, product=i['product'], quantity=i['quantity']
                )

            # Clear bag
            request.session['bag'] = {}

            # Save checkout details back to profile if requested
            if request.POST.get('save_info') == 'on':
                profile = _get_user_profile(request.user)
                if profile:
                    # These field names assume Boutique Ado-style UserProfile defaults
                    profile.default_phone_number = order.phone_number
                    profile.default_country = order.country
                    profile.default_postcode = order.postcode
                    profile.default_town_or_city = order.town_or_city
                    profile.default_street_address1 = order.street_address1
                    profile.default_street_address2 = order.street_address2
                    profile.save()

            # Best-effort confirmation email
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
        # If invalid, fall through to re-render the page with errors
        order_form = order_form
    else:
        # GET: prefill form from profile/account where possible
        initial = {}
        profile = _get_user_profile(request.user)
        if profile:
            initial = {
                'full_name': (request.user.get_full_name() or '').strip(),
                'email': (request.user.email or '').strip(),
                'phone_number': profile.default_phone_number,
                'country': profile.default_country,
                'postcode': profile.default_postcode,
                'town_or_city': profile.default_town_or_city,
                'street_address1': profile.default_street_address1,
                'street_address2': profile.default_street_address2,
            }
        else:
            initial = {
                'full_name': (request.user.get_full_name() or '').strip(),
                'email': (request.user.email or '').strip(),
            }
        order_form = OrderForm(initial=initial)

    # --- Create PaymentIntent (both GET and POST-invalid) ---
    client_secret = ''
    do_stripe = STRIPE_ENABLED
    if do_stripe:
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(total * 100),  # cents
                currency=getattr(settings, 'STRIPE_CURRENCY', 'eur'),
                metadata={
                    'bag': json.dumps(request.session.get('bag', {})),
                    'username': request.user.username,
                },
            )
            client_secret = intent.client_secret
        except stripe.error.AuthenticationError:
            messages.error(request, "Stripe keys look invalid. Continuing without payment for now.")
            do_stripe = False
        except Exception:
            messages.error(request, "Stripe is temporarily unavailable. Continuing without payment.")
            do_stripe = False

    if not do_stripe:
        # Tell the template not to render Elements; form will still submit & create an Order
        client_secret = "test_secret_disabled"
        messages.warning(request, "Stripe is not configured. Running in no-payment demo mode.")

    return render(request, 'checkout/checkout.html', {
        'order_form': order_form,  # <-- template expects this key
        'items': items,
        'total': total,
        'stripe_public_key': getattr(settings, "STRIPE_PUBLIC_KEY", ""),
        'client_secret': client_secret,
    })


@login_required
def checkout_success(request, order_id):
    """
    Simple success page showing the order reference.
    """
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'checkout/checkout_success.html', {'order': order})


@login_required
def my_orders(request):
    """
    List a user's orders (assumes Order has a created_on DateTimeField).
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_on')
    return render(request, 'checkout/my_orders.html', {'orders': orders})
