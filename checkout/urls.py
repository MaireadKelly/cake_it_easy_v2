from django.urls import path

from . import views, webhooks

urlpatterns = [
    path("", views.checkout, name="checkout"),
    path("orders/", views.my_orders, name="my_orders"),
    path("orders/<int:order_id>/", views.order_detail, name="order_detail"),
    path(
        "success/<int:order_id>/",
        views.checkout_success,
        name="checkout_success",
    ),
    path("wh/", webhooks.stripe_webhook, name="stripe_webhook"),
]
