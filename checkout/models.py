from django.contrib.auth.models import User
from django.db import models

from products.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    full_name = models.CharField(max_length=80)
    email = models.EmailField()
    phone_number = models.CharField(max_length=32, blank=True)
    country = models.CharField(max_length=2, blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    town_or_city = models.CharField(max_length=40, blank=True)
    street_address1 = models.CharField(max_length=80, blank=True)
    street_address2 = models.CharField(max_length=80, blank=True)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stripe_pid = models.CharField(max_length=254, blank=True)
    original_bag = models.TextField(blank=True)
    paid = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    lineitem_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order_id})"