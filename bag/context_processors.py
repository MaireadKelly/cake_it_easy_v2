from decimal import Decimal
from products.models import Product

FREE_DELIVERY_THRESHOLD = Decimal('50.00')
STANDARD_DELIVERY = Decimal('5.00')

def bag_contents(request):
    """
    Session schema (simple):
        session['bag'] = { "<product_id>": quantity, ... }

    Returns keys compatible with your existing templates:
        - bag_items: list of { item_id, product, quantity, line_total }
        - product_count: int
        - total: Decimal               (a.k.a. subtotal)
        - bag_total: Decimal           (alias of total for walkthrough compatibility)
        - delivery: Decimal
        - free_delta: Decimal          (amount left to free delivery)
        - grand_total: Decimal
    """
    bag = request.session.get('bag', {})

    items = []
    product_count = 0
    total = Decimal('0.00')

    for item_id, quantity in bag.items():
        try:
            pid = int(item_id)
            qty = int(quantity)
        except (TypeError, ValueError):
            continue

        product = Product.objects.filter(pk=pid).first()
        if not product:
            continue

        line_total = (product.price or Decimal('0.00')) * qty
        total += line_total
        product_count += qty
        items.append({
            'item_id': pid,
            'product': product,
            'quantity': qty,
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
        'total': total,              # subtotal
        'bag_total': total,          # alias for compatibility with templates/walkthrough
        'delivery': delivery,
        'free_delta': free_delta,
        'grand_total': grand_total,
    }

# Backward-compat: if settings still reference 'bag.context_processors.bag_totals'
def bag_totals(request):
    return bag_contents(request)
