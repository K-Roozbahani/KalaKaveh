from django.contrib import admin

from carts.models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

    fields = (
        "variant",
        "quantity",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "variant",
    )

    show_change_link = True


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "status",
        "coupon",
        "items_count",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "status",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "user__phone_number",
        "session_key",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "user",
        "coupon",
    )

    inlines = (
        CartItemInline,
    )

    date_hierarchy = "created_at"

    ordering = (
        "-created_at",
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        return queryset.select_related(
            "user",
            "coupon",
        ).prefetch_related(
            "items",
        )

    @admin.display(description="تعداد آیتم‌ها")
    def items_count(self, obj):
        return obj.items.count()


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cart",
        "variant",
        "quantity",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "variant__sku",
        "variant__product__name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "cart",
        "variant",
    )

    ordering = (
        "-created_at",
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        return queryset.select_related(
            "cart",
            "variant",
            "variant__product",
        )
