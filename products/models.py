from django.db import models
from django.utils.html import format_html
from django.utils.text import slugify
import uuid


def generate_sku() -> str:
    """Return a short, unique, upper-case SKU."""
    return uuid.uuid4().hex[:8].upper()


class Category(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True,
        related_name='subcategories', on_delete=models.SET_NULL
    )
    slug = models.SlugField(max_length=60, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name if self.friendly_name else self.name

    def save(self, *args, **kwargs):
        # auto-create slug from name if missing
        if not self.slug and self.name:
            self.slug = slugify(self.name)[:60]
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)  # auto-filled in save()
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    featured = models.BooleanField(default=False)
    is_custom = models.BooleanField(default=False)
    is_accessory = models.BooleanField(default=False)
    is_offer = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def image_preview(self):
        if self.image:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit:cover;" />',
                self.image.url
            )
        return "No Image"
    image_preview.short_description = 'Preview'

    def save(self, *args, **kwargs):
        """
        Auto-assign an SKU if missing.
        Uses a short uppercase UUID slice; loops on the (extremely unlikely) collision.
        """
        if not self.sku:
            new = generate_sku()
            while type(self).objects.filter(sku=new).exists():
                new = generate_sku()
            self.sku = new
        super().save(*args, **kwargs)
