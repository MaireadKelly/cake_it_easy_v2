from decimal import Decimal

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product, ProductOption

# -----------------------------------------------------------------------------
# Deposit identity
# -----------------------------------------------------------------------------
# Best practice: identify the deposit product by SKU (stable, not user-facing).
# Set this to match the SKU shown in Django Admin for "Custom Cake Deposit".
DEPOSIT_SKU = "CUST-DEP"  

# Fallback (works if SKU not set). Keep exact admin name.
DEPOSIT_NAME_FALLBACK = "Custom Cake Deposit"


def _is_deposit_product(product: Product) -> bool:
    """
    Return True if this product is the single-quantity deposit item.

    Uses SKU first (recommended). Falls back to name if SKU not set.
    """
    sku = (getattr(product, "sku", "") or "").strip()
    name = (getattr(product, "name", "") or "").strip()
    return (sku and sku == DEPOSIT_SKU) or (name == DEPOSIT_NAME_FALLBACK)


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

    Special case:
    - "Custom Cake Deposit" can only be added once (quantity forced to 1).
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

    # -------------------------------------------------------------------------
    # Deposit rule: allow only one deposit in the bag
    # -------------------------------------------------------------------------
    if _is_deposit_product(product):
        # Force quantity = 1 always
        if key in bag:
            # Already added — do not add again
            bag[key] = 1
            request.session.modified = True
            messages.info(
                request,
                "Custom cake deposit is already in your bag (quantity is limited to 1).",
            )
            return redirect(request.POST.get("redirect_url") or "view_bag")

        bag[key] = 1
        request.session.modified = True
        messages.success(request, f"Added 1 × {product.name} to your bag.")
        return redirect(request.POST.get("redirect_url") or "view_bag")

    # Normal behaviour for all other products
    bag[key] = bag.get(key, 0) + qty
    request.session.modified = True

    if option:
        messages.success(
            request,
            f"Added {qty} × {product.name} ({option.label}) to your bag.",
        )
    else:
        messages.success(request, f"Added {qty} × {product.name} to your bag.")

    return redirect(request.POST.get("redirect_url") or "view_bag")


def adjust_bag(request, product_id):
    """
    Adjust the quantity of a product/option in the bag; 0 removes it.

    Special case:
    - "Custom Cake Deposit" quantity is capped at 1 (cannot be increased).
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

    # Deposit rule enforcement (even if user tampers with POST qty)
    if _is_deposit_product(product):
        if qty <= 0:
            bag.pop(key, None)
            request.session.modified = True
            messages.info(request, f"Removed {product.name}")
            return redirect("view_bag")

        bag[key] = 1
        request.session.modified = True
        messages.info(
            request,
            f"{product.name} quantity is limited to 1.",
        )
        return redirect("view_bag")

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
    """
    if request.method != "POST":
        return redirect("view_bag")

    code = (request.POST.get("code") or "").strip().upper()
    if not code:
        messages.error(request, "Please enter a discount code.")
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
