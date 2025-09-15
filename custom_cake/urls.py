from django.urls import path
from . import views

urlpatterns = [
    # Make /custom_cake/ land on the public create form (best UX)
    path("", views.create_custom_cake, name="custom_cake_index"),

    # existing routes
    path("create/", views.create_custom_cake, name="create_custom_cake"),
    path("my-cakes/", views.custom_cake_list, name="custom_cake_list"),
    path("edit/<int:pk>/", views.update_custom_cake, name="update_custom_cake"),
    path("delete/<int:pk>/", views.delete_custom_cake, name="delete_custom_cake"),
]
