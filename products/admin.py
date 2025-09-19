from django.contrib import admin
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('friendly_name', 'name', 'parent')
    list_filter = ('parent',)
    search_fields = ('name', 'friendly_name')
    ordering = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Product admin:
    - SKU is read-only (auto-generated in Product.save()).
    - Quick search by name/SKU/description.
    - Useful list filters & preview.
    """
    list_display = ('name', 'sku', 'category', 'price', 'featured',
                    'is_custom', 'is_accessory', 'is_offer', 'image_preview')
    list_filter = ('category', 'featured', 'is_custom', 'is_accessory', 'is_offer')
    search_fields = ('name', 'sku', 'description')
    readonly_fields = ('image_preview', 'sku')
    ordering = ('sku',)

    # Control field order in the edit page (read-only shown at the end)
    fields = (
        'name', 'category', 'description', 'price',
        'image', 'featured', 'is_custom', 'is_accessory', 'is_offer',
        'image_preview', 'sku',  # read-only
    )
