from decimal import Decimal

def bag_totals(request):
    bag = request.session.get('bag', {})
    count = 0
    for _, qty in bag.items():
        try:
            count += int(qty)
        except Exception:
            pass
    # Header shows count; precise totals calculated in checkout
    return {"bag_count": count, "bag_total": Decimal("0.00")}