from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from shipping.models import (
    Shipment,
    ShippingMethod,
)


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "estimated_days",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "-id",
    )

    list_per_page = 50

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            _("اطلاعات روش ارسال"),
            {
                "fields": (
                    "name",
                    "price",
                    "estimated_days",
                    "is_active",
                ),
            },
        ),
        (
            _("اطلاعات سیستمی"),
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "shipping_method",
        "tracking_code",
        "status",
        "shipped_at",
        "delivered_at",
        "created_at",
    )

    list_filter = (
        "status",
        "shipping_method",
        "created_at",
    )

    search_fields = (
        "tracking_code",
        "order__order_number",
    )

    ordering = (
        "-id",
    )

    list_per_page = 50

    autocomplete_fields = (
        "order",
        "shipping_method",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "shipped_at",
        "delivered_at",
    )

    fieldsets = (
        (
            _("اطلاعات مرسوله"),
            {
                "fields": (
                    "order",
                    "shipping_method",
                    "tracking_code",
                    "status",
                    "description",
                ),
            },
        ),
        (
            _("زمان‌بندی ارسال"),
            {
                "fields": (
                    "shipped_at",
                    "delivered_at",
                ),
            },
        ),
        (
            _("اطلاعات سیستمی"),
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    show_full_result_count = False