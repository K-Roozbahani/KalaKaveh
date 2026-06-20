from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

    fields = (
        "product",
        "variant",
        "quantity",
        "price",
        "discount_amount",
        "final_price",
    )

    readonly_fields = (
        "product",
        "variant",
        "quantity",
        "price",
        "discount_amount",
        "final_price",
    )

    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "user",
        "status",
        "subtotal",
        "discount_amount",
        "shipping_method",
        "shipping_cost",
        "total_amount",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "order_number",
        "user__phone_number",
        "user__first_name",
        "user__last_name",
    )

    readonly_fields = (
        "order_number",
        "address_snapshot",
        "subtotal",
        "discount_amount",
        "shipping_cost",
        "total_amount",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "اطلاعات سفارش",
            {
                "fields": (
                    "order_number",
                    "user",
                    "status",
                )
            },
        ),
        (
            "اطلاعات مالی",
            {
                "fields": (
                    "subtotal",
                    "discount_amount",
                    "shipping_cost",
                    "total_amount",
                )
            },
        ),
        (
            "آدرس سفارش",
            {
                "fields": (
                    "address_snapshot",
                )
            },
        ),
        (
            "توضیحات",
            {
                "fields": (
                    "note",
                )
            },
        ),
        (
            "زمان‌ها",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
        (
            "روش ارسال",
            {
                "fields": (
                    "shipping_method_snapshot",
                )
            }
        )
    )

    autocomplete_fields = (
        "shipping_method",
    )

    inlines = [OrderItemInline]

    date_hierarchy = "created_at"

    ordering = ("-created_at",)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "product",
        "variant",
        "quantity",
        "final_price",
    )

    search_fields = (
        "order__order_number",
        "product__name",
    )

    list_select_related = (
        "order",
        "product",
        "variant",
    )

    readonly_fields = (
        "order",
        "product",
        "variant",
        "quantity",
        "price",
        "discount_amount",
        "final_price",
        "product_snapshot",
    )

    ordering = ("-id",)

    def has_delete_permission(self, request, obj=None):
        return False