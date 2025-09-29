from django.contrib.auth.models import User
from django.db import models
from decimal import Decimal

from products.models import Product
# Optional FK – only importable if you added ProductOption in products app
try:
    from products.models import ProductOption
except Exception:
    ProductOption = None


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

    # Order totals
    order_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    # NEW: discount
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    discount_code = models.CharField(max_length=40, blank=True)

    # Stripe / meta
    stripe_pid = models.CharField(max_length=254, blank=True)
    original_bag = models.TextField(blank=True)
    paid = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    # which option (e.g., Box of 6/12). Nullable for products without options.
    option = models.ForeignKey(
        ProductOption, null=True, blank=True, on_delete=models.SET_NULL
    )
    quantity = models.IntegerField(default=1)
    # unit pack price captured at time of order
    lineitem_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    lineitem_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        unit = self.lineitem_price
        if not unit or unit <= 0:
            if self.option and hasattr(self.option, 'price') and self.option.price:
                unit = self.option.price
            else:
                unit = self.product.price
            self.lineitem_price = unit
        self.lineitem_total = unit * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        label = f" ({self.option.label})" if self.option else ""
        return f"{self.quantity} x {self.product.name}{label} (Order {self.order_id})"
