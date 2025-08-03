from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    """
    A view to display all products.
    Allows future extension to add sorting, filtering, and search.
    """
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, product_id):
    """
    A view to show individual product details.
    """
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)
