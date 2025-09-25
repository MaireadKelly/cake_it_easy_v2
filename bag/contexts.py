from decimal import Decimal

from products.models import Product


def bag_contents(request):
    bag = request.session.get('bag', {})
    items = []
    total = Decimal('0.00')


    for pid, qty in bag.items():
        product = Product.objects.get(pk=int(pid))
        line_total = product.price * qty
        items.append({
            'product': product,
            'quantity': qty,
            'line_total': line_total,
        })
        total += line_total


    return {
        'bag_items': items,
        'bag_total': total,
        'bag_count': sum(bag.values()) if bag else 0,
    }