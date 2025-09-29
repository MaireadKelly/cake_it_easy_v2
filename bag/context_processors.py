from decimal import Decimal
from products.models import Product, ProductOption

FREE_DELIVERY_THRESHOLD = Decimal("50.00")
STANDARD_DELIVERY = Decimal("5.00")


def _is_cupcake(product: Product) -> bool:
    cat = getattr(product, "category", None)
    if not cat:
        return False
    # Match by slug if present, else by name
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
        # pack_price() expected to return numeric -> Decimal
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
    total = Decimal("0.00")

    for key, quantity in bag.items():
        # Parse key safely
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
        total += line_total
        product_count += qty

        per_unit = None
        if option and getattr(option, "quantity", None):
            per_unit = (unit_price / Decimal(option.quantity))

        items.append({
            "key": key,
            "product": product,
            "option": option,        # None unless cupcakes with valid option
            "quantity": qty,         # number of boxes if option present
            "unit_price": unit_price,
            "per_unit": per_unit,    # price per cupcake (Decimal) or None
            "line_total": line_total,
        })

    if product_count == 0 or total >= FREE_DELIVERY_THRESHOLD:
        delivery = Decimal("0.00")
        free_delta = Decimal("0.00")
    else:
        delivery = STANDARD_DELIVERY
        free_delta = FREE_DELIVERY_THRESHOLD - total

    grand_total = total + delivery

    # Expose both keys so templates using either continue to work
    return {
        "items": items,              # <-- new alias
        "bag_items": items,          # existing key
        "product_count": product_count,
        "total": total,
        "bag_total": total,
        "delivery": delivery,
        "free_delta": free_delta,
        "grand_total": grand_total,
    }


def bag_totals(request):
    return bag_contents(request)
