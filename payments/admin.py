from django.contrib import admin

from payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    مدیریت پرداخت‌ها در پنل ادمین.
    """

    # -----------------------------
    # List View
    # -----------------------------
    list_display = (
        "id",
        "order",
        "gateway",
        "authority",
        "ref_id",
        "amount",
        "status",
        "paid_at",
        "created_at",
    )

    list_select_related = (
        "order",
        "order__user",
    )

    list_filter = (
        "status",
        "gateway",
        "created_at",
        "paid_at",
    )

    date_hierarchy = "created_at"

    ordering = (
        "-created_at",
    )

    # -----------------------------
    # Search
    # -----------------------------
    search_fields = (
        "authority",
        "ref_id",
        "order__order_number",
        "order__user__phone_number",
    )

    # -----------------------------
    # Readonly Fields
    # -----------------------------
    readonly_fields = (
        "authority",
        "ref_id",
        "amount",
        "paid_at",
        "created_at",
        "updated_at",
    )

    # -----------------------------
    # Performance
    # -----------------------------
    show_full_result_count = False

    # -----------------------------
    # Detail View
    # -----------------------------
    fieldsets = (
        (
            "اطلاعات سفارش",
            {
                "fields": (
                    "order",
                    "amount",
                )
            },
        ),
        (
            "اطلاعات درگاه",
            {
                "fields": (
                    "gateway",
                    "authority",
                    "ref_id",
                )
            },
        ),
        (
            "وضعیت پرداخت",
            {
                "fields": (
                    "status",
                    "paid_at",
                    "failure_reason",
                )
            },
        ),
        (
            "اطلاعات سیستمی",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    # -----------------------------
    # Prevent Accidental Deletion
    # -----------------------------
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser