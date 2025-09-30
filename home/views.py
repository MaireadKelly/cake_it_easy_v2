from django.shortcuts import render
from django.views.generic import TemplateView

from products.models import Product


def index(request):
    products = Product.objects.filter(featured=True)[:8]
    return render(
        request,
        "home/index.html",
        {"products": products},
    )


class AboutView(TemplateView):
    template_name = "home/about.html"
