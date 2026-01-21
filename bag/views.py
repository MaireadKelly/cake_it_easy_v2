from decimal import Decimal
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from checkout.models import Order
from products.models import Product, ProductOption


def _get_bag(session):
    """Ensure a bag dict exists in the session and return it."""
    return session.setdefault("bag", {})


def view_bag(request):
    """Render the bag page (items & totals come from context processor)."""
    return render(request, "bag/bag.html")


def add_to_bag(request, product_id):
    """
    Add a product (with optional ProductOption) to the bag.
    Options are ONLY applied to Cupcakes.
    """
    if request.method != "POST":
        return redirect("product_detail", product_id=product_id)

    product = get_object_or_404(Product, pk=product_id)

    # Parse quantity safely
    try:
        qty = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        qty = 1
    qty = max(1, qty)

    bag = _get_bag(request.session)

    # Cupcakes check (by slug or name)
    cat = getattr(product, "category", None)
    cat_slug = (getattr(cat, "slug", "") or "").lower()
    cat_name = (getattr(cat, "name", "") or "").lower()
    is_cupcake = cat_slug == "cupcakes" or cat_name == "cupcakes"

    option = None
    if is_cupcake:
        posted_opt = request.POST.get("option_id") or request.POST.get("box_size")
        if posted_opt:
            option = ProductOption.objects.filter(
                pk=posted_opt, product=product
            ).first()

    # Key includes option only for valid cupcake option
    key = f"{product_id}_{option.id}" if option else str(product_id)

    # Normal behaviour for all products (including Custom Cake Deposit)
    bag[key] = bag.get(key, 0) + qty
    request.session.modified = True

    if option:
        messages.success(
            request,
            f"Added {qty} × {product.name} ({option.label}) to your bag.",
        )
    else:
        messages.success(request, f"Added {qty} × {product.name} to your bag.")

    # Respect redirect_url if provided, otherwise go to bag
    return redirect(request.POST.get("redirect_url") or "view_bag")


def adjust_bag(request, product_id):
    """
    Adjust the quantity of a product/option in the bag; 0 removes it.
    """
    if request.method != "POST":
        return redirect("view_bag")

    product = get_object_or_404(Product, pk=product_id)
    option_id = request.POST.get("option_id")

    try:
        qty = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        qty = 1

    bag = _get_bag(request.session)

    key = str(product_id)
    option = None
    if option_id:
        option = ProductOption.objects.filter(
            pk=option_id, product=product
        ).first()
        if option:
            key = f"{product_id}_{option.id}"

    # Normal behaviour
    if qty > 0:
        bag[key] = qty
        msg = f"Updated {product.name}"
        if option:
            msg += f" ({option.label})"
        messages.info(request, f"{msg} quantity to {qty}.")
    else:
        bag.pop(key, None)
        msg = f"Removed {product.name}"
        if option:
            msg += f" ({option.label})"
        messages.info(request, msg)

    request.session.modified = True
    return redirect("view_bag")


def remove_from_bag(request, product_id):
    """Remove a product/option entirely from the bag."""
    product = get_object_or_404(Product, pk=product_id)
    option_id = request.POST.get("option_id")

    bag = _get_bag(request.session)
    key = str(product_id)

    option = None
    if option_id:
        option = ProductOption.objects.filter(
            pk=option_id, product=product
        ).first()
        if option:
            key = f"{product_id}_{option.id}"

    if key in bag:
        bag.pop(key)
        request.session.modified = True
        msg = f"Removed {product.name}"
        if option:
            msg += f" ({option.label})"
        messages.info(request, msg)

    return redirect("view_bag")

# ---------- discount code endpoints ----------

def apply_discount(request):
    """
    Accepts POST with 'code'. MVP supports:
      WELCOME10 -> 10% off subtotal (before delivery).

    Stores {'code': CODE, 'amount': Decimal} in session['discount'].

    WELCOME10 can only be used once per registered user.
    """
    if request.method != "POST":
        return redirect("view_bag")

    code = (request.POST.get("code") or "").strip().upper()
    if not code:
        messages.error(request, "Please enter a discount code.")
        return redirect("view_bag")

    # Enforce single-use per registered user
    if code == "WELCOME10" and request.user.is_authenticated:
        already_used = Order.objects.filter(
            user=request.user,
            discount_code="WELCOME10",
            paid=True,
        ).exists()

        if already_used:
            messages.info(
                request,
                "WELCOME10 has already been used on your account. Please use a different code.",
            )
            return redirect("view_bag")

    # Compute against current subtotal via context processor
    from .context_processors import bag_contents

    ctx = bag_contents(request)
    subtotal = ctx.get("total", Decimal("0.00"))

    amount = Decimal("0.00")
    if code == "WELCOME10":
        amount = (subtotal * Decimal("0.10")).quantize(Decimal("0.01"))

    if amount <= 0:
        messages.error(request, "This code is invalid or your bag is empty.")
        request.session.pop("discount", None)
        request.session.modified = True
        return redirect("view_bag")

    request.session["discount"] = {"code": code, "amount": str(amount)}
    request.session.modified = True
    messages.success(
        request, f"Discount code '{code}' applied: -€{amount:.2f}"
    )
    return redirect("view_bag")


def remove_discount(request):
    """Remove any applied discount from session."""
    request.session.pop("discount", None)
    request.session.modified = True
    messages.info(request, "Discount removed.")
    return redirect("view_bag")
