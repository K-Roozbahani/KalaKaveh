from django.db.models import Q, QuerySet
from django.utils import timezone

from discounts.models import (
    Discount,
    DiscountScope,
    Coupon,
    CouponUsage,
)

from products.models import (
    Product,
    ProductVariant,
    Category,
    Brand,
)


# =====================================================
# Discount
# =====================================================

def get_discount_by_id(
    *,
    discount_id: int,
) -> Discount:
    """
    دریافت تخفیف بر اساس شناسه
    """

    return Discount.objects.get(
        pk=discount_id,
    )


def get_active_discounts() -> QuerySet[Discount]:
    """
    دریافت تمام تخفیف‌های فعال
    """

    now = timezone.now()

    return (
        Discount.objects
        .filter(
            is_active=True,
            start_date__lte=now,
            end_date__gte=now,
        )
    )


def get_active_discount_by_id(
    *,
    discount_id: int,
) -> Discount:
    """
    دریافت تخفیف فعال
    """

    now = timezone.now()

    return (
        Discount.objects
        .get(
            pk=discount_id,
            is_active=True,
            start_date__lte=now,
            end_date__gte=now,
        )
    )


# =====================================================
# Coupon
# =====================================================

def get_coupon_by_code(
    *,
    code: str,
) -> Coupon:
    """
    دریافت کوپن بر اساس کد
    """

    return (
        Coupon.objects
        .select_related("discount")
        .get(
            code=code,
        )
    )


def get_active_coupon_by_code(
    *,
    code: str,
) -> Coupon:
    """
    دریافت کوپن فعال
    """

    now = timezone.now()

    return (
        Coupon.objects
        .select_related("discount")
        .get(
            code=code,
            is_active=True,
            start_date__lte=now,
            end_date__gte=now,
        )
    )


# =====================================================
# Coupon Usage
# =====================================================

def get_coupon_usage(
    *,
    coupon: Coupon,
):
    """
    سوابق استفاده از کوپن
    """

    return (
        CouponUsage.objects
        .filter(
            coupon=coupon,
        )
    )


def has_user_used_coupon(
    *,
    coupon: Coupon,
    user,
) -> bool:
    """
    آیا کاربر قبلاً از کوپن استفاده کرده است؟
    """

    return (
        CouponUsage.objects
        .filter(
            coupon=coupon,
            user=user,
        )
        .exists()
    )


# =====================================================
# Discount Scopes
# =====================================================

def get_product_scopes(
    *,
    product: Product,
):
    """
    تخفیف‌های مستقیم محصول
    """

    return (
        DiscountScope.objects
        .select_related("discount")
        .filter(
            product=product,
        )
    )


def get_variant_scopes(
    *,
    variant: ProductVariant,
):
    """
    تخفیف‌های مستقیم تنوع محصول
    """

    return (
        DiscountScope.objects
        .select_related("discount")
        .filter(
            variant=variant,
        )
    )


def get_category_scopes(
    *,
    category: Category,
):
    """
    تخفیف‌های دسته‌بندی
    """

    return (
        DiscountScope.objects
        .select_related("discount")
        .filter(
            category=category,
        )
    )


def get_brand_scopes(
    *,
    brand: Brand,
):
    """
    تخفیف‌های برند
    """

    return (
        DiscountScope.objects
        .select_related("discount")
        .filter(
            brand=brand,
        )
    )


# =====================================================
# Pricing Engine Selectors
# =====================================================

def get_applicable_discount_scopes(
    *,
    variant: ProductVariant,
):
    """
    تمام تخفیف‌های موثر روی یک تنوع محصول
    """

    now = timezone.now()

    return (
        DiscountScope.objects
        .select_related(
            "discount",
        )
        .filter(
            discount__is_active=True,
            discount__start_date__lte=now,
            discount__end_date__gte=now,
        )
        .filter(
            Q(
                variant=variant,
            )
            |
            Q(
                product=variant.product,
            )
            |
            Q(
                category=variant.product.category,
            )
            |
            Q(
                brand=variant.product.brand,
            )
        )
        .order_by(
            "-discount__priority",
        )
    )


def get_highest_priority_discount(
    *,
    variant: ProductVariant,
):
    """
    بالاترین اولویت تخفیف موثر روی محصول
    """

    return (
        get_applicable_discount_scopes(
            variant=variant,
        )
        .first()
    )

def get_variant_available_discounts(
    *,
    variant: ProductVariant,
) -> QuerySet[Discount]:
    """
    دریافت تمام تخفیف‌های قابل اعمال روی تنوع محصول.

    ترتیب اولویت در این مرحله اعمال نمی‌شود
    و فقط تمام Discount های معتبر برگردانده می‌شوند.
    """

    return (
        get_active_discounts()
        .filter(
            scopes__variant=variant,
        )
        .distinct()
        .order_by(
            "-priority",
            "-id",
        )
    )


def get_variant_active_discount(
    *,
    variant: ProductVariant,
):
    """
    دریافت بهترین تخفیف فعال.

    جهت سازگاری با کدهای قبلی نگه داشته شده است.
    """

    return (
        get_variant_available_discounts(
            variant=variant,
        )
        .first()
    )