﻿from decimal import Decimal
from products.models import Product, ProductOption

FREE_DELIVERY_THRESHOLD = Decimal("50.00")
STANDARD_DELIVERY = Decimal("5.00")


def _is_cupcake(product: Product) -> bool:
    cat = getattr(product, "category", None)
    if not cat:
        return False
    slug = getattr(cat, "slug", "") or ""
    name = getattr(cat, "name", "") or ""
    return slug.lower() == "cupcakes" or name.lower() == "cupcakes"


def _pack_price(product: Product, option: ProductOption | None) -> Decimal:
    """
    Unit price used for a line item:
      - Cupcakes with option: per-box price from option.pack_price()
      - Everything else: product.price
    """
    if option:
        return Decimal(option.pack_price())
    return Decimal(product.price or 0)


def bag_contents(request):
    """
    session['bag'] keys:
      "<product_id>"                 -> simple product
      "<product_id>_<option_id>"     -> ONLY cupcakes (box option)
    """
    bag = request.session.get("bag", {})
    items = []
    product_count = 0
    subtotal = Decimal("0.00")

    for key, quantity in bag.items():
        try:
            pid_str, opt_str = (str(key).split("_", 1) + [None])[:2]
            pid = int(pid_str)
            opt_id = int(opt_str) if opt_str else None
            qty = int(quantity)
        except (TypeError, ValueError):
            continue

        product = Product.objects.select_related("category").filter(pk=pid).first()
        if not product:
            continue

        option = None
        if opt_id and _is_cupcake(product):
            option = ProductOption.objects.filter(pk=opt_id, product_id=pid).first()

        unit_price = _pack_price(product, option)   # price per box for cupcakes; else product.price
        line_total = unit_price * qty
        subtotal += line_total
        product_count += qty

        per_unit = None
        if option and getattr(option, "quantity", None):
            per_unit = (unit_price / Decimal(option.quantity))

        items.append({
            "key": key,
            "product": product,
            "option": option,
            "quantity": qty,         # number of boxes if option present
            "unit_price": unit_price,
            "per_unit": per_unit,    # price per cupcake (Decimal) or None
            "line_total": line_total,
        })

    # Delivery
    if product_count == 0 or subtotal >= FREE_DELIVERY_THRESHOLD:
        delivery = Decimal("0.00")
        free_delta = Decimal("0.00")
    else:
        delivery = STANDARD_DELIVERY
        free_delta = FREE_DELIVERY_THRESHOLD - subtotal

    # --- Discount from session ---
    disc = request.session.get('discount') or {}
    try:
        discount_amount = Decimal(str(disc.get('amount', '0') or '0'))
    except Exception:
        discount_amount = Decimal('0.00')
    discount_code = disc.get('code') or ''

    if discount_amount < 0:
        discount_amount = Decimal('0.00')
    if discount_amount > subtotal:
        discount_amount = subtotal

    total_after_discount = subtotal - discount_amount
    grand_total = total_after_discount + delivery

    return {
        "items": items,              # alias
        "bag_items": items,
        "product_count": product_count,
        "total": subtotal,           # pre-discount subtotal
        "bag_total": subtotal,
        "delivery": delivery,
        "free_delta": free_delta,
        "discount_amount": discount_amount,
        "discount_code": discount_code,
        "grand_total": grand_total,
    }


def bag_totals(request):
    return bag_contents(request)
