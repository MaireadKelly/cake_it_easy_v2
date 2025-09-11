from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ("lineitem_total",)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "email", "order_total", "paid", "created_on")
    list_filter = ("paid", "created_on")
    search_fields = ("id", "full_name", "email", "stripe_pid")
    readonly_fields = ("stripe_pid", "original_bag", "order_total", "created_on", "paid")
    inlines = (OrderLineItemInline,)
    ordering = ("-created_on",)        # newest first
    date_hierarchy = "created_on"      # sidebar date drilldown
