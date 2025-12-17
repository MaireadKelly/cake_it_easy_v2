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

    # Columns in list view (quick fulfilment overview)
    list_display = (
        "id",
        "created_on",
        "full_name",
        "email",
        "town_or_city",
        "postcode",
        "order_total",
        "discount_amount",
        "paid",
    )
    list_filter = ("paid", "created_on")
    search_fields = ("id", "email", "full_name", "stripe_pid", "postcode")
    ordering = ("-created_on",)

    # Read-only / system fields
    readonly_fields = (
        "order_total",
        "discount_amount",
        "stripe_pid",
        "original_bag",
        "created_on",
    )

    # Bulk actions
    actions = [mark_paid]

    # Tidy edit form layout
    fieldsets = (
        (
            "Customer",
            {"fields": ("user", "full_name", "email", "phone_number")},
        ),
        (
            "Delivery Address",
            {
                "fields": (
                    "street_address1",
                    "street_address2",
                    "town_or_city",
                    "county",
                    "postcode",
                    "country",
                )
            },
        ),
        (
            "Discount",
            {"fields": ("discount_code", "discount_amount")},
        ),
        (
            "Payment / Stripe",
            {
                "fields": (
                    "paid",
                    "stripe_pid",
                    "original_bag",
                    "created_on",
                )
            },
        ),
        (
            "Totals",
            {"fields": ("order_total",)},
        ),
    )
