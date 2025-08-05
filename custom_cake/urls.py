from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_custom_cake, name='create_custom_cake'),
    path('my-cakes/', views.custom_cake_list, name='custom_cake_list'),
]
