from decimal import Decimal

def bag_totals(request):
    bag = request.session.get('bag', {})
    total = Decimal('0.00')
    count = 0
    for _, qty in bag.items():
        try:
            q = int(qty)
        except Exception:
            q = 0
        count += q
    # Header shows count; precise totals are computed in checkout
    return {'bag_count': count, 'bag_total': total}
