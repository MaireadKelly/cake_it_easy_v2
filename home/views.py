# home/views.py
from django.shortcuts import render

from products.models import Product


def index(request):
    products = Product.objects.filter(featured=True)[:8]
    return render(request, "home/index.html", {"products": products})

from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = "home/about.html"
