from django.urls import path

from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("cakes/", views.product_cakes, name="product_cakes"),
    path(
        "accessories/", views.product_accessories, name="product_accessories"
    ),
    path("offers/", views.product_offers, name="product_offers"),
    # Admin-only CRUD
    path("add/", views.add_product, name="add_product"),
    path("<int:product_id>/edit/", views.edit_product, name="edit_product"),
    path(
        "<int:product_id>/delete/", views.delete_product, name="delete_product"
    ),
    path("<int:product_id>/", views.product_detail, name="product_detail"),
]
