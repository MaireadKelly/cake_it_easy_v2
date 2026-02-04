from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm
from .models import Category, Product


# ----------------------------
# Helpers
# ----------------------------


def _apply_search_sort(queryset, request):
    """
    Apply query params consistently:
      - ?q= search term
      - ?sort= name|price|category
      - ?direction= asc|desc
    """
    q = request.GET.get("q", "").strip()
    if q:
        queryset = queryset.filter(
            Q(name__icontains=q)
            | Q(description__icontains=q)
            | Q(category__name__icontains=q)
            | Q(category__friendly_name__icontains=q)
        )

    sort = request.GET.get("sort", "")
    direction = request.GET.get("direction", "asc").lower()

    # Harden direction so weird values don't break ordering logic
    if direction not in ("asc", "desc"):
        direction = "asc"

    sortkey = None
    if sort == "name":
        queryset = queryset.annotate(lower_name=Lower("name"))
        sortkey = "lower_name"
    elif sort == "price":
        sortkey = "price"
    elif sort == "category":
        sortkey = "category__name"

    if sortkey:
        if direction == "desc":
            sortkey = f"-{sortkey}"
        queryset = queryset.order_by(sortkey)

    return queryset, q, sort, direction


def _ids_for_category_and_children(slug):
    """Return ([parent.id] + child_ids, parent_category). If slug missing: ([], None)."""
    try:
        parent = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        return [], None
    child_ids = list(parent.subcategories.values_list("id", flat=True))
    return [parent.id] + child_ids, parent


# ----------------------------
# Catalog views
# ----------------------------


def product_list(request):
    """All products, optional ?category=a,b,c filtering (CSV of slugs)."""
    qs = Product.objects.all()

    cat_param = request.GET.get("category", "").strip()
    slugs = [s for s in cat_param.split(",") if s]
    if slugs:
        qs = qs.filter(category__slug__in=slugs)

    qs, q, sort, direction = _apply_search_sort(qs, request)

    context = {
        "products": qs,
        "page_title": "All Products",
        "request_get": request.GET,
        "search_term": q,
        "current_sort": sort,
        "current_direction": direction,
        "current_categories": Category.objects.filter(slug__in=slugs),
        "selected_slugs": slugs,
    }
    return render(request, "products/product_list.html", context)


def product_cakes(request):
    """
    Cakes landing:
      - Products in parent 'cakes' + its children
      - Chips: only 'Cupcakes' (walkthrough-simple)
      - Optional narrowing via ?category=cupcakes
    """
    ids, cakes_cat = _ids_for_category_and_children("cakes")
    qs = (
        Product.objects.filter(category_id__in=ids)
        if ids
        else Product.objects.none()
    )

    cat_param = request.GET.get("category", "").strip()
    slugs = [s for s in cat_param.split(",") if s]
    if slugs:
        qs = qs.filter(category__slug__in=slugs)

    qs, q, sort, direction = _apply_search_sort(qs, request)

    cupcakes = Category.objects.filter(slug="cupcakes").first()
    context = {
        "products": qs,
        "page_title": "Cakes",
        "active_category": cakes_cat,
        "subcategories": [cupcakes] if cupcakes else [],
        "request_get": request.GET,
        "search_term": q,
        "current_sort": sort,
        "current_direction": direction,
        "current_categories": Category.objects.filter(slug__in=slugs),
        "selected_slugs": slugs,
    }
    return render(request, "products/product_list.html", context)


def product_accessories(request):
    """
    Accessories landing:
      - Products in parent 'accessories' + its children
      - Chips: 'Balloons' and 'Candles' only
      - Optional narrowing via ?category=balloons or candles
    """
    ids, acc_cat = _ids_for_category_and_children("accessories")
    qs = (
        Product.objects.filter(category_id__in=ids)
        if ids
        else Product.objects.none()
    )

    cat_param = request.GET.get("category", "").strip()
    slugs = [s for s in cat_param.split(",") if s]
    if slugs:
        qs = qs.filter(category__slug__in=slugs)

    qs, q, sort, direction = _apply_search_sort(qs, request)

    balloons = Category.objects.filter(slug="balloons").first()
    candles = Category.objects.filter(slug="candles").first()
    context = {
        "products": qs,
        "page_title": "Accessories",
        "active_category": acc_cat,
        "subcategories": [c for c in (balloons, candles) if c],
        "request_get": request.GET,
        "search_term": q,
        "current_sort": sort,
        "current_direction": direction,
        "current_categories": Category.objects.filter(slug__in=slugs),
        "selected_slugs": slugs,
    }
    return render(request, "products/product_list.html", context)


def product_offers(request):
    """Special offers flagged with is_offer=True."""
    qs, q, sort, direction = _apply_search_sort(
        Product.objects.filter(is_offer=True), request
    )
    context = {
        "products": qs,
        "page_title": "Special Offers",
        "request_get": request.GET,
        "search_term": q,
        "current_sort": sort,
        "current_direction": direction,
        "current_categories": [],
        "selected_slugs": [],
    }
    return render(request, "products/product_list.html", context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, "products/product_detail.html", {"product": product})


# ----------------------------
# Staff CRUD
# ----------------------------


@staff_member_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Added {product.name}")
            return redirect("product_detail", product_id=product.id)
    else:
        form = ProductForm()
    return render(request, "products/product_form.html", {"form": form})


@staff_member_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Updated {product.name}")
            return redirect("product_detail", product_id=product.id)
    else:
        form = ProductForm(instance=product)
    return render(
        request,
        "products/product_form.html",
        {"form": form, "product": product},
    )


@staff_member_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        name = product.name
        product.delete()
        messages.info(request, f"Deleted {name}")
        return redirect("product_list")
    return render(
        request, "products/product_confirm_delete.html", {"product": product}
    )
