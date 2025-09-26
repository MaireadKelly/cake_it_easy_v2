from django.urls import path
from .views import AboutView
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("about/", AboutView.as_view(), name="about"),
]
