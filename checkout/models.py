from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models

from products.models import Product

# Optional FK – only importable if ProductOption exists in products app
try:
    from products.models import ProductOption
except ImportError:
    ProductOption = None


class Order(models.Model):
    """
    Order model for Cake It Easy.

    Differences from the Boutique Ado walkthrough:
    - Uses `user` FK instead of `user_profile`.
    - Stores `order_total` and `discount_amount` separately.
    - `grand_total` is provided as a @property for compatibility
      with templates / webhook logic that expect a single total.
    """

    # User and contact info
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL
    )
    full_name = models.CharField(max_length=80)
    email = models.EmailField()
    phone_number = models.CharField(max_length=32, blank=True)

    # Address
    country = models.CharField(max_length=2, blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    town_or_city = models.CharField(max_length=40, blank=True)
    street_address1 = models.CharField(max_length=80, blank=True)
    street_address2 = models.CharField(max_length=80, blank=True)
    county = models.CharField(max_length=80, blank=True)

    # Order totals
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    discount_code = models.CharField(max_length=40, blank=True)

    # Stripe / metadata
    stripe_pid = models.CharField(max_length=254, blank=True)
    original_bag = models.TextField(blank=True)
    paid = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    @property
    def grand_total(self):
        """
        Convenience property to mirror Boutique Ado's `grand_total`.
        Returns the final amount after any discount.
        """
        return (self.order_total or Decimal("0.00")) - (
            self.discount_amount or Decimal("0.00")
        )

    def update_total(self):
        """
        Recalculate the order_total from related line items.

        Discount logic is intentionally separate and stored in
        discount_amount to keep totals explicit and auditable.
        """
        self.order_total = (
            self.lineitems.aggregate(
                total=models.Sum("lineitem_total")
            )["total"] or Decimal("0.00")
        )
        self.save(update_fields=["order_total"])

    def __str__(self):
        return f"Order {self.id}"



class OrderLineItem(models.Model):
    """
    Line items for each order.
    Supports optional ProductOption (e.g. box sizes / variants)
    and automatically calculates lineitem_total from quantity
    and either the option price or base product price.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="lineitems",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
    )

    # Product option (nullable if not used)
    option = models.ForeignKey(
        ProductOption,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    quantity = models.IntegerField(default=1)

    # Price and total
    lineitem_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    lineitem_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False,
    )

    def save(self, *args, **kwargs):
        """
        Ensure lineitem_price is set from:
        - ProductOption.price if present
        - else Product.price
        Then multiply by quantity to get lineitem_total.
        """
        unit = self.lineitem_price

        if not unit or unit <= 0:
            if (
                self.option
                and hasattr(self.option, "price")
                and self.option.price
            ):
                unit = self.option.price
            else:
                unit = self.product.price
            self.lineitem_price = unit

        self.lineitem_total = unit * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        label = f" ({self.option.label})" if self.option else ""
        return (
            f"{self.quantity} x {self.product.name}"
            f"{label} (Order {self.order_id})"
        )
