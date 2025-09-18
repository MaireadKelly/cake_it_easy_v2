from decimal import Decimal
from products.models import Product

def bag_totals(request):
    """
    Provide bag totals to all templates (used by the header mini-total).
    Expected session shape: request.session['bag'] = { "<product_id>": quantity }
    """
    bag = request.session.get('bag', {})

    total = Decimal('0.00')
    product_count = 0
    bag_items = []

    for item_id, quantity in bag.items():
        # session keys are strings; ensure ints for DB lookup and math
        pid = int(item_id)
        qty = int(quantity)

        try:
            product = Product.objects.get(pk=pid)
        except Product.DoesNotExist:
            # If something stale is in the session, skip it
            continue

        line_total = (product.price or Decimal('0.00')) * qty
        total += line_total
        product_count += qty

        bag_items.append({
            "item_id": pid,
            "quantity": qty,
            "product": product,
            "line_total": line_total,
        })

    # Return BOTH names so whichever your header uses will work
    context = {
        "bag_items": bag_items,
        "product_count": product_count,
        "total": total,
        "grand_total": total,  # many headers read {{ grand_total }}
        "bag_total": total,
        "bag_count": product_count, 
    }
    return context
