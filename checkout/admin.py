from django.contrib import admin

from .models import Order, OrderLineItem


class OrderLineItemInline(admin.TabularInline):
    model = OrderLineItem
    extra = 0
    readonly_fields = ("lineitem_total",)


@admin.action(description="Mark selected orders as paid")
def mark_paid(modeladmin, request, queryset):
    queryset.update(paid=True)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderLineItemInline]

    # columns in list view
    list_display = ("id", "created_on", "user", "email", "order_total", "paid")
    list_filter = ("paid", "created_on")
    search_fields = ("id", "email", "full_name", "stripe_pid")
    ordering = ("-created_on",)

    # read-only/calculated fields
    readonly_fields = ("order_total", "stripe_pid", "original_bag", "created_on")

    # bulk action
    actions = [mark_paid]

    # tidy edit form layout
    fieldsets = (
        ("Customer", {"fields": ("user", "full_name", "email", "phone_number")}),
        ("Address", {"fields": ("country", "postcode", "town_or_city", "street_address1", "street_address2")}),
        ("Order", {"fields": ("order_total", "paid", "stripe_pid", "original_bag", "created_on")}),
    )
