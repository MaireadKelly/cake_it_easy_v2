from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product

def _get_bag(session):
    """Ensure a bag dict exists in the session and return it."""
    return session.setdefault('bag', {})

def view_bag(request):
    """Render the bag page (items & totals come from context processor)."""
    return render(request, 'bag/bag.html')

def add_to_bag(request, product_id):
    """Add a quantity of the specified product to the bag."""
    if request.method != 'POST':
        return redirect('product_detail', product_id=product_id)

    product = get_object_or_404(Product, pk=product_id)

    try:
        qty = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        qty = 1
    qty = max(1, qty)

    bag = _get_bag(request.session)
    pid = str(product_id)
    bag[pid] = bag.get(pid, 0) + qty
    request.session.modified = True

    messages.success(request, f'Added {qty} × {product.name} to your bag.')
    redirect_url = request.POST.get('redirect_url') or 'view_bag'
    return redirect(redirect_url)

def adjust_bag(request, product_id):
    """Set the quantity for a product; 0 removes it."""
    if request.method != 'POST':
        return redirect('view_bag')

    product = get_object_or_404(Product, pk=product_id)

    try:
        qty = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        qty = 1

    bag = _get_bag(request.session)
    pid = str(product_id)

    if qty > 0:
        bag[pid] = qty
        messages.info(request, f'Updated {product.name} quantity to {qty}.')
    else:
        bag.pop(pid, None)
        messages.info(request, f'Removed {product.name} from your bag.')

    request.session.modified = True
    return redirect('view_bag')

def remove_from_bag(request, product_id):
    """Remove a product entirely from the bag."""
    product = get_object_or_404(Product, pk=product_id)
    bag = _get_bag(request.session)
    pid = str(product_id)

    if pid in bag:
        bag.pop(pid)
        request.session.modified = True
        messages.info(request, f'Removed {product.name} from your bag.')

    return redirect('view_bag')
