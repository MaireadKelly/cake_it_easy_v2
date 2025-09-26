import os
from decimal import Decimal

from products.models import Product  # uses your existing Product model

DEPOSIT_SKU = "CUST-DEP"

def get_or_create_deposit_product():
    """
    Returns a Product representing the custom-cake deposit.
    Creates it if missing. Price is taken from env CUSTOM_CAKE_DEPOSIT (default 20.00).
    """
    prod = Product.objects.filter(sku=DEPOSIT_SKU).first()
    if prod:
        return prod

    amount = Decimal(os.getenv("CUSTOM_CAKE_DEPOSIT", "20.00"))
    prod = Product.objects.create(
        name="Custom Cake Deposit",
        sku=DEPOSIT_SKU,
        description="Non-refundable design & booking deposit for a custom cake.",
        price=amount,
        featured=False,
        is_custom=True,
        is_accessory=False,
        is_offer=False,
    )
    return prod
