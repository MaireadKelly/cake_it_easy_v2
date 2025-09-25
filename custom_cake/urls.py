from django.urls import path

from . import views

urlpatterns = [
    # Logged-in user's list (used by your navbar)
    path('my-cakes/', views.custom_cake_list, name='custom_cake_list'),

    # CRUD (login required; owner or staff can edit/delete)
    path('create/', views.custom_cake_create, name='custom_cake_create'),
    path('<int:pk>/', views.custom_cake_detail, name='custom_cake_detail'),
    path('<int:pk>/edit/', views.custom_cake_edit, name='custom_cake_edit'),
    path('<int:pk>/delete/', views.custom_cake_delete, name='custom_cake_delete'),
]
