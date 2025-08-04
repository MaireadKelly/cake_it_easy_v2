# products/admin.py
from django.contrib import admin
from .models import Product, Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_custom', 'is_accessory', 'is_offer', 'featured', 'image_preview')
    list_filter = ('category', 'is_custom', 'is_accessory', 'is_offer', 'featured')
    search_fields = ('name', 'sku', 'description')
    readonly_fields = ('image_preview',)

    ordering = ('sku',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('friendly_name', 'name', 'parent')
    list_filter = ('parent',)
    search_fields = ('name', 'friendly_name')
