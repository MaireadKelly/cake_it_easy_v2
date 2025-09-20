from django.contrib import admin
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('friendly_name', 'name', 'slug', 'parent')
    list_filter = ('parent',)
    search_fields = ('name', 'friendly_name', 'slug')
    ordering = ('name',)
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'price', 'featured',
                    'is_custom', 'is_accessory', 'is_offer', 'image_preview')
    list_filter = ('category', 'featured', 'is_custom', 'is_accessory', 'is_offer')
    search_fields = ('name', 'sku', 'description')
    readonly_fields = ('image_preview', 'sku')
    ordering = ('sku',)
    fields = (
        'name', 'category', 'description', 'price',
        'image', 'featured', 'is_custom', 'is_accessory', 'is_offer',
        'image_preview', 'sku',
    )
