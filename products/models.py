import uuid

from django.db import models
from django.utils.html import format_html
from django.utils.text import slugify


def generate_sku() -> str:
    return uuid.uuid4().hex[:8].upper()


class Category(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="subcategories",
        on_delete=models.SET_NULL,
    )
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name or self.name

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = (
                slugify(self.friendly_name or self.name)[:60]
                or f"category-{self.pk or ''}"
            )
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()

    # Treat as unit price (e.g., per cupcake)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    image = models.ImageField(
        upload_to="products/",
        null=True,
        blank=True,
    )

    featured = models.BooleanField(default=False)
    is_custom = models.BooleanField(default=False)
    is_accessory = models.BooleanField(default=False)
    is_offer = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def image_preview(self):
        image = getattr(self, "image", None)
        if image and hasattr(image, "url"):
            return format_html(
                '<img src="{}" width="100" height="100" '
                'style="object-fit:cover;" />',
                image.url,
            )
        return "No Image"

    image_preview.short_description = "Preview"

    def save(self, *args, **kwargs):
        if not self.sku:
            new_sku = generate_sku()
            while type(self).objects.filter(sku=new_sku).exists():
                new_sku = generate_sku()
            self.sku = new_sku
        super().save(*args, **kwargs)

    # ---- Helpers for UI badges / labels ----

    def min_pack_option(self):
        """Return the ProductOption with the smallest quantity (if any)."""
        opts = list(self.options.all())
        return min(opts, key=lambda o: o.quantity) if opts else None

    def min_pack_price(self):
        """Return the price for the smallest box size (Decimal or None)."""
        opt = self.min_pack_option()
        return opt.pack_price() if opt else None

    def min_pack_size(self):
        """Return the smallest box quantity (int or None)."""
        opt = self.min_pack_option()
        return opt.quantity if opt else None


class ProductOption(models.Model):
    """
    Per-product purchasable option (e.g., 'Box of 4/6/12/18').

    If 'price' is left blank, we compute:
        product.price * quantity
    """

    product = models.ForeignKey(
        Product,
        related_name="options",
        on_delete=models.CASCADE,
    )
    label = models.CharField(max_length=50)  # e.g. "Box of 6"
    quantity = models.PositiveIntegerField(default=6)  # e.g. 4, 6, 12, 18
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
    )  # Optional override
    is_default = models.BooleanField(default=False)

    class Meta:
        ordering = ["quantity"]
        unique_together = ("product", "quantity")

    def __str__(self):
        return f"{self.product.name} - {self.label}"

    def pack_price(self):
        """
        Return the total pack price:
        - Use self.price if set,
        - Else compute as product.price * quantity.
        """
        if self.price is not None:
            return self.price
        return (self.product.price or 0) * self.quantity
