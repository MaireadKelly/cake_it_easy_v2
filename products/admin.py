from django.contrib import admin
from .models import Product, Category
from django.utils.text import Truncator

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

    actions = ['fill_missing_descriptions']
    def fill_missing_descriptions(self, request, queryset):
        updated = 0
        for p in queryset:
            if not (p.description or '').strip():
                cat = getattr(p.category, 'friendly_name', None) or getattr(p.category, 'name', '') or ''
                p.description = f"{p.name}. {('Category: ' + cat) if cat else ''} Delicious and freshly made."
                p.save(update_fields=['description'])
                updated += 1
        self.message_user(request, f"Filled {updated} product descriptions.")
    fill_missing_descriptions.short_description = "Fill missing descriptions (simple)"
