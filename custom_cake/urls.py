from django.urls import path
from . import views

urlpatterns = [
    # List & detail
    path("", views.custom_cake_list, name="custom_cake_list"),
    path("<int:pk>/", views.custom_cake_detail, name="custom_cake_detail"),
    # Create / Update / Delete – expose BOTH name styles:
    path("create/", views.custom_cake_create, name="custom_cake_create"),
    path("create/", views.custom_cake_create, name="create_custom_cake"),
    path("<int:pk>/edit/", views.custom_cake_edit, name="custom_cake_edit"),
    path("<int:pk>/edit/", views.custom_cake_edit, name="custom_cake_update"),
    path("<int:pk>/edit/", views.custom_cake_edit, name="update_custom_cake"),
    path(
        "<int:pk>/delete/", views.custom_cake_delete, name="custom_cake_delete"
    ),
    path(
        "<int:pk>/delete/", views.custom_cake_delete, name="delete_custom_cake"
    ),
    path("design-your-own/", views.design_your_own, name="design_your_own"),
]
