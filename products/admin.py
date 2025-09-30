from django.contrib import admin

from .models import Category, Product, ProductOption


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("friendly_name", "name", "slug", "parent")
    list_filter = ("parent",)
    search_fields = ("name", "friendly_name", "slug")
    ordering = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 1
    fields = ("label", "quantity", "price", "is_default")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "sku",
        "category",
        "price",
        "featured",
        "is_custom",
        "is_accessory",
        "is_offer",
        "image_preview",
    )
    list_filter = (
        "category",
        "featured",
        "is_custom",
        "is_accessory",
        "is_offer",
    )
    search_fields = ("name", "sku", "description")
    readonly_fields = ("image_preview", "sku")
    ordering = ("sku",)
    fields = (
        "name",
        "category",
        "description",
        "price",
        "image",
        "featured",
        "is_custom",
        "is_accessory",
        "is_offer",
        "image_preview",
        "sku",
    )
    inlines = [ProductOptionInline]

    actions = ["fill_missing_descriptions"]

    def fill_missing_descriptions(self, request, queryset):
        """
        Fill in blank descriptions with a default value using the product name
        and category.
        """
        updated = 0

        for product in queryset:
            if not (product.description or "").strip():
                category = (
                    getattr(product.category, "friendly_name", None)
                    or getattr(product.category, "name", "")
                )

                description = f"{product.name}."
                if category:
                    description += f" Category: {category}."
                description += " Delicious and freshly made."

                product.description = description
                product.save(update_fields=["description"])
                updated += 1

        self.message_user(
            request,
            f"Filled {updated} product description(s)."
        )

    fill_missing_descriptions.short_description = (
        "Fill missing descriptions (simple)"
    )
