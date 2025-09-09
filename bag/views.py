from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product

def view_bag(request):
    # Minimal page with checkout button; items are shown on checkout page
    return render(request, 'bag/bag.html')


def add_to_bag(request, product_id):
    if request.method != 'POST':
        return redirect('product_detail', product_id=product_id)
    product = get_object_or_404(Product, pk=product_id)
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
    return redirect('view_bag')
