from django.shortcuts import render
from products.models import Product

""" A view to return to the home page """
def home(request):
    products = Product.objects.all()
    return render(request, 'home/index.html', {'products': products})
