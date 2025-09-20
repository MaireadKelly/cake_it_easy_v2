from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm
from .models import Category, Product


def _apply_search_sort(products, request):
    """Apply search (?q=) and sorting (?sort=&direction=) consistently."""
    query = request.GET.get('q', '').strip()
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    sort = request.GET.get('sort', '')
    direction = request.GET.get('direction', 'asc').lower()
    sortkey = 'id'
    if sort == 'name':
        products = products.annotate(lower_name=Lower('name'))
        sortkey = 'lower_name'
    elif sort == 'price':
        sortkey = 'price'
    elif sort == 'category':
        products = products.annotate(cat_name=Lower('category__friendly_name'))
        sortkey = 'cat_name'
    if direction == 'desc':
        sortkey = f'-{sortkey}'
    products = products.order_by(sortkey)

    return products, query, sort, direction


def product_list(request):
    """
    Default list page.
    Supports:
      - ?category=cakes,accessories (CSV; uses Category.slug/name/friendly_name)
      - ?q=…
      - ?sort=name|price|category & ?direction=asc|desc
    """
    products = Product.objects.all()
    selected_qs = Category.objects.none()

    # CSV category filter (keep working to avoid breaking links), but custom-cakes is NOT part of products.
    if 'category' in request.GET and request.GET['category'].strip():
        tokens = [t.strip() for t in request.GET['category'].split(',') if t.strip()]
        # If someone enters custom-cakes, we *do not* show products; we’ll just ignore it here.
        tokens = [t for t in tokens if t != 'custom-cakes']
        if tokens:
            selected_qs = Category.objects.filter(
                Q(slug__in=tokens) | Q(name__in=tokens) | Q(friendly_name__in=tokens)
            ).distinct()
            if selected_qs.exists():
                products = products.filter(category__in=selected_qs)

    products, query, sort, direction = _apply_search_sort(products, request)

    context = {
        'products': products,
        'all_categories': Category.objects.exclude(slug='custom-cakes'),  # never show custom-cakes chip
        'current_categories': selected_qs,
        'selected_slugs': list(selected_qs.values_list('slug', flat=True)),
        'search_term': query,
        'current_sort': sort,
        'current_direction': direction,
        'current_sorting': f'{sort}_{direction}' if sort else '',
        'request_get': request.GET,
    }
    return render(request, 'products/product_list.html', context)


# ---- Dedicated nav targets ----

def product_cakes(request):
    """Cakes (normal catalogue items) – show only category slug 'cakes' if it exists; else show all non-accessory offers off."""
    qs = Product.objects.all()
    # If you created a 'Cakes' category, prefer it:
    try:
        cakes_cat = Category.objects.get(slug='cakes')
        qs = qs.filter(category=cakes_cat)
    except Category.DoesNotExist:
        # Fallback: exclude accessories if you use that category; otherwise leave as-is
        qs = qs.exclude(category__slug='accessories')
    qs, query, sort, direction = _apply_search_sort(qs, request)
    context = {
        'products': qs,
        'all_categories': Category.objects.exclude(slug__in=['custom-cakes']),  # keep chips simple
        'current_categories': Category.objects.filter(slug='cakes') if 'cakes' in [c.slug for c in Category.objects.all()] else Category.objects.none(),
        'selected_slugs': ['cakes'],
        'search_term': query,
        'current_sort': sort,
        'current_direction': direction,
        'current_sorting': f'{sort}_{direction}' if sort else '',
        'request_get': request.GET,
    }
    return render(request, 'products/product_list.html', context)


def product_accessories(request):
    """Accessories category page."""
    qs = Product.objects.filter(category__slug='accessories')
    qs, query, sort, direction = _apply_search_sort(qs, request)
    context = {
        'products': qs,
        'all_categories': Category.objects.exclude(slug__in=['custom-cakes']),
        'current_categories': Category.objects.filter(slug='accessories'),
        'selected_slugs': ['accessories'],
        'search_term': query,
        'current_sort': sort,
        'current_direction': direction,
        'current_sorting': f'{sort}_{direction}' if sort else '',
        'request_get': request.GET,
    }
    return render(request, 'products/product_list.html', context)


def product_offers(request):
    """Special Offers (uses your boolean flag on Product)."""
    qs = Product.objects.filter(is_offer=True)
    qs, query, sort, direction = _apply_search_sort(qs, request)
    context = {
        'products': qs,
        'all_categories': Category.objects.exclude(slug__in=['custom-cakes']),
        'current_categories': Category.objects.none(),
        'selected_slugs': [],
        'search_term': query,
        'current_sort': sort,
        'current_direction': direction,
        'current_sorting': f'{sort}_{direction}' if sort else '',
        'request_get': request.GET,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/product_detail.html', {'product': product})


# ---- Dedicated nav targets ----

@staff_member_required
def add_product(request):
    """Create a new product (staff only)."""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" created.')
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form, 'mode': 'add'})

@staff_member_required
def edit_product(request, product_id):
    """Edit an existing product (staff only)."""
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{product.name}" updated.')
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'mode': 'edit', 'product': product})

@staff_member_required
def delete_product(request, product_id):
    """Delete a product (staff only, with confirmation)."""
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f'Product "{name}" deleted.')
        return redirect('product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})