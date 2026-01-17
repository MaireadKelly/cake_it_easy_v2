from django.contrib import admin
from .models import CustomCake


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
        "short_description",
        "created_on",
    )

    list_filter = ("occasion", "needed_date", "created_on")
    search_fields = ("id", "user__username", "name", "description")
    ordering = ("-created_on",)

    # Make timestamps read-only (edit form)
    readonly_fields = ("created_on",)

    fieldsets = (
        ("Customer", {"fields": ("user", "name")}),
        ("Request Details", {"fields": ("occasion", "flavor", "filling", "size", "inscription", "needed_date")}),
        ("Notes", {"fields": ("description",)}),
        ("Media", {"fields": ("image",)}),
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
