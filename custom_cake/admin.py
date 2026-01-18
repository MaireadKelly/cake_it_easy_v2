from django.contrib import admin
from .models import CustomCake
from django.utils.html import format_html



@admin.register(CustomCake)
class CustomCakeAdmin(admin.ModelAdmin):
    """
    Admin config so staff can manage CustomCake requests efficiently.
    Ensures the 'description' (notes) is visible and searchable.
    """

    # Show key info in the list view (includes a short description preview)
    list_display = (
        "id",
        "user",
        "name",
        "occasion",
        "needed_date",
        "image_preview",
        "inscription",
        "short_description",
        "created_on",
    )

    list_filter = ("occasion", "needed_date", "created_on")
    search_fields = ("id", "user__username", "name", "description")
    ordering = ("-created_on",)

    # Make timestamps read-only (edit form)
    readonly_fields = ("created_on", "image_preview")

    fieldsets = (
        ("Customer", {"fields": ("user", "name")}),
        ("Request Details", {"fields": ("occasion", "flavor", "filling", "size", "inscription", "needed_date")}),
        ("Notes", {"fields": ("description",)}),
        ("Media", {"fields": ("image", "image_preview")}),
        ("System", {"fields": ("created_on",)}),
    )

    @admin.display(description="Notes")
    def short_description(self, obj):
        """
        Preview the description in the list page without it taking over the table.
        """
        if not obj.description:
            return ""
        text = obj.description.strip()
        return text[:60] + ("…" if len(text) > 60 else "")
    
    @admin.display(description="Image Preview")
    def image_preview(self, obj):
        """
        Display a small preview of the uploaded cake image in admin.
        """
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; border-radius: 6px;" />',
                obj.image.url
            )
        return "No image"

