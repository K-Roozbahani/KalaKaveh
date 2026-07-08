from django.contrib import admin

from .models import (
    Discount,
    DiscountScope,
    Coupon,
    CouponUsage,
)

#برای اهداف تخغیف
class DiscountTargetInline(admin.TabularInline):
    model = DiscountScope
    extra = 1


#برای کدهای تخفیف
class CouponInline(admin.TabularInline):
    model = Coupon
    extra = 0


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "discount_type",
        "value",
        "priority",
        "is_active",
        "start_date",
        "end_date",
    )

    list_filter = (
        "discount_type",
        "is_active",
        "start_date",
        "end_date",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "-priority",
        "-id",
    )

    inlines = (
        DiscountTargetInline,
        CouponInline,
    )

    readonly_fields = (
        "created_at",
    )


@admin.register(DiscountScope)
class DiscountTargetAdmin(admin.ModelAdmin):

    list_display = (
        "discount",
        "variant",
        "product",
        "category",
        "brand",
    )

    list_filter = (
        "discount",
    )

    search_fields = (
        "discount__name",
        "product__name",
        "variant__sku",
    )


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "discount",
        "usage_limit",
        "used_count",
        "is_active",
        "start_date",
        "end_date",
    )

    list_filter = (
        "is_active",
        "discount",
    )

    search_fields = (
        "code",
    )

    ordering = (
        "-id",
    )


@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):

    list_display = (
        "coupon",
        "user",
        "order",
        "used_at",
    )

    list_filter = (
        "coupon",
        "used_at",
    )

    search_fields = (
        "coupon__code",
        "user__username",
    )

    readonly_fields = (
        "coupon",
        "user",
        "order",
        "used_at",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

