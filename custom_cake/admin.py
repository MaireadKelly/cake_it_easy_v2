from django.contrib import admin
from django.utils.html import format_html

from .models import CustomCake


@admin.register(CustomCake)
class CustomCakeAdmin(admin.ModelAdmin):
    # List view columns
    list_display = (
        "name",
        "flavor",
        "filling",
        "size",
        "created_on",
        "user",
        "needed_date",
        "image_preview",
    )
    list_display_links = ("name",)

    # Filters and search
    list_filter = (
        "occasion",
        "flavor",
        "filling",
        "size",
        "needed_date",
        "created_on",
    )
    search_fields = ("name", "description", "inscription", "user__username")

    # Usability & performance
    ordering = ("-created_on",)
    readonly_fields = ("created_on", "image_preview")
    list_per_page = 25
    save_on_top = True
    date_hierarchy = "created_on"
    autocomplete_fields = ["user"]
    list_select_related = ("user",)

    # Admin form layout
    fieldsets = (
        (
            "Request",
            {
                "fields": (
                    "user",
                    "name",
                    "description",
                    "occasion",
                    "flavor",
                    "filling",
                    "size",
                    "inscription",
                    "image",
                )
            },
        ),
        ("Meta", {"fields": ("created_on", "image_preview")}),
    )

    def image_preview(self, obj):
        if getattr(obj, "image", None):
            try:
                url = obj.image.url
                return format_html(
                    '<img src="{}" width="60" height="60" '
                    'style="object-fit:cover; border-radius:6px;" />',
                    url,
                )
            except Exception:
                return "—"
        return "—"

    image_preview.short_description = "Preview"
