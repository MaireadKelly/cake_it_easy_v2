from decimal import Decimal
from products.models import Product, ProductOption

FREE_DELIVERY_THRESHOLD = Decimal('50.00')
STANDARD_DELIVERY = Decimal('5.00')


def _pack_price(product, option: ProductOption | None) -> Decimal:
    if option:
        return Decimal(option.pack_price())
    return Decimal(product.price or 0)


def bag_contents(request):
    """
    session['bag']: { "<product_id>[_<option_id>]": quantity, ... }
    quantity = number of boxes when an option is present.
    """
    bag = request.session.get('bag', {})
    items = []
    product_count = 0
    total = Decimal('0.00')

    for key, quantity in bag.items():
        try:
            parts = str(key).split('_')
            pid = int(parts[0])
            opt_id = int(parts[1]) if len(parts) == 2 else None
            qty = int(quantity)
        except (TypeError, ValueError):
            continue

        product = Product.objects.filter(pk=pid).first()
        if not product:
            continue

        option = None
        if opt_id:
            option = ProductOption.objects.filter(pk=opt_id, product_id=pid).first()

        unit_price = _pack_price(product, option)  # price per **box**
        line_total = unit_price * qty
        total += line_total
        product_count += qty

        per_unit = None
        if option and option.quantity:
            per_unit = (unit_price / Decimal(option.quantity))

        items.append({
            'key': key,
            'product': product,
            'option': option,
            'quantity': qty,       # number of boxes if option present
            'unit_price': unit_price,     # price per box
            'per_unit': per_unit,         # price per cupcake (Decimal or None)
            'line_total': line_total,
        })

    if product_count == 0 or total >= FREE_DELIVERY_THRESHOLD:
        delivery = Decimal('0.00')
        free_delta = Decimal('0.00')
    else:
        delivery = STANDARD_DELIVERY
        free_delta = FREE_DELIVERY_THRESHOLD - total

    grand_total = total + delivery

    return {
        'bag_items': items,
        'product_count': product_count,
        'total': total,
        'bag_total': total,
        'delivery': delivery,
        'free_delta': free_delta,
        'grand_total': grand_total,
    }


def bag_totals(request):
    return bag_contents(request)
