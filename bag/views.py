from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product, ProductOption


def _get_bag(session):
    """Ensure a bag dict exists in the session and return it."""
    return session.setdefault("bag", {})


def view_bag(request):
    """Render the bag page (items & totals come from context processor)."""
    return render(request, "bag/bag.html")


def add_to_bag(request, product_id):
    """Add a product (with optional ProductOption) to the bag."""
    if request.method != "POST":
        return redirect("product_detail", product_id=product_id)

    product = get_object_or_404(Product, pk=product_id)
    option_id = request.POST.get("option_id")

    try:
        qty = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        qty = 1
    qty = max(1, qty)

    bag = _get_bag(request.session)

    key = str(product_id)
    option = None
    if option_id:
        option = ProductOption.objects.filter(pk=option_id, product=product).first()
        if option:
            key = f"{product_id}_{option.id}"

    bag[key] = bag.get(key, 0) + qty
    request.session.modified = True

    if option:
        messages.success(
            request, f"Added {qty} × {product.name} ({option.label}) to your bag."
        )
    else:
        messages.success(request, f"Added {qty} × {product.name} to your bag.")

    return redirect(request.POST.get("redirect_url") or "view_bag")


def adjust_bag(request, product_id):
    """Adjust the quantity of a product/option in the bag; 0 removes it."""
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
        option = ProductOption.objects.filter(pk=option_id, product=product).first()
        if option:
            key = f"{product_id}_{option.id}"

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
        option = ProductOption.objects.filter(pk=option_id, product=product).first()
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
