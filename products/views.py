from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from django.db.models.functions import Lower
from django.contrib.admin.views.decorators import staff_member_required

from .models import Product, Category
from .forms import ProductForm


def product_list(request):
    """
    Supports:
      - ?category=cupcakes,cakes   (CSV; matches Category.name OR friendly_name)
      - ?q=choc                    (search in name + description)
      - ?sort=name|price|category  (case-insensitive for name/category)
      - ?direction=asc|desc
    Preserves the rest of the query string so the UI can keep state.
    """
    products = Product.objects.all()
    query = None
    categories = None
    sort = request.GET.get('sort', '')
    direction = request.GET.get('direction', 'asc').lower()

    # ---- Category filter (CSV; accept name or friendly_name) ----
    selected = []
    if 'category' in request.GET and request.GET['category'].strip():
        raw = request.GET['category']
        selected = [s.strip() for s in raw.split(',') if s.strip()]
        # filter by either field
        products = products.filter(
            Q(category__name__in=selected) | Q(category__friendly_name__in=selected)
        ).distinct()
        categories = Category.objects.filter(
            Q(name__in=selected) | Q(friendly_name__in=selected)
        ).distinct()

    # ---- Search ----
    if 'q' in request.GET:
        query = request.GET['q']
        if not query.strip():
            messages.error(request, "You didn't enter any search criteria!")
            return redirect('product_list')
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    # ---- Sorting (case-insensitive for name/category) ----
    sortkey = 'id'
    if sort == 'name':
        products = products.annotate(lower_name=Lower('name'))
        sortkey = 'lower_name'
    elif sort == 'price':
        sortkey = 'price'
    elif sort == 'category':
        # sort by friendly_name for nicer UX
        products = products.annotate(cat_name=Lower('category__friendly_name'))
        sortkey = 'cat_name'

    if direction == 'desc':
        sortkey = f'-{sortkey}'
    products = products.order_by(sortkey)

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,    # queryset of matched categories (if any)
        'selected_categories': selected,     # raw list of chosen categories
        'current_sort': sort,
        'current_direction': direction,
        'current_sorting': f'{sort}_{direction}' if sort else '',
        'request_get': request.GET,          # lets the template preserve other params
        'all_categories': Category.objects.all(),  # chips without extra context processor
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/product_detail.html', {'product': product})


# -------- RBAC: Admin-only CRUD --------

@staff_member_required
def add_product(request):
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
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f'Product "{name}" deleted.')
        return redirect('product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})
