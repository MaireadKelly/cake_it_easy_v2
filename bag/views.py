from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product

def view_bag(request):
    return render(request, 'bag/bag.html')

def add_to_bag(request, product_id):
    """
    Add a quantity of the specified product to the shopping bag.
    Improvements:
      - Guard non-POST access (redirect back to product detail)
      - Floor quantity at 1 to avoid 0/negative adds
    """
    # Only allow POST to modify the bag
    if request.method != 'POST':
        return redirect('product_detail', product_id=product_id)

    product = get_object_or_404(Product, pk=product_id)

    # Floor at 1
    try:
        qty = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        qty = 1
    qty = max(1, qty)

    bag = request.session.get('bag', {})
    pid = str(product_id)
    bag[pid] = bag.get(pid, 0) + qty
    request.session['bag'] = bag

    messages.success(request, f"Added {qty} × {product.name} to your bag.")
    # For the PASS demo flow, go straight to checkout
    return redirect('view_bag')
