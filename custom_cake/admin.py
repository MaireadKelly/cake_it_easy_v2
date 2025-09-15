# File: custom_cake/admin.py
from django.contrib import admin
from .models import CustomCake


@admin.register(CustomCake)
class CustomCakeAdmin(admin.ModelAdmin):
    # columns in the list view
    list_display = ("name", "flavor", "filling", "size", "created_on", "user")
    list_display_links = ("name",)  # clicking the name opens the edit page

    # quick filters and search
    list_filter = ("occasion", "flavor", "filling", "size", "created_on")
    search_fields = ("name", "description", "inscription", "user__username")

    # ordering & read-only
    ordering = ("-created_on",)
    readonly_fields = ("created_on",)

    # tidy edit form layout
    fieldsets = (
        ("Request", {
            "fields": (
                "user", "name", "description",
                "occasion", "flavor", "filling", "size", "inscription"
            )
        }),
        ("Meta", {"fields": ("created_on",)}),
    )
