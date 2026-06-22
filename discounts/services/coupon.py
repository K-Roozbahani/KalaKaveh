from decimal import Decimal

from django.db import transaction

from discounts.models import (
    Coupon,
    CouponUsage,
)

from discounts.selectors import (
    has_user_used_coupon,
)

from discounts.validators import (
    validate_coupon_is_active,
    validate_coupon_usage_limit,
    validate_user_has_not_used_coupon,
)


def validate_coupon(
    *,
    coupon: Coupon,
    user,
) -> Coupon:
    """
    اعتبارسنجی کوپن
    """

    validate_coupon_is_active(
        coupon=coupon,
    )

    validate_coupon_usage_limit(
        coupon=coupon,
    )

    validate_user_has_not_used_coupon(
        has_used=has_user_used_coupon(
            coupon=coupon,
            user=user,
        )
    )

    return coupon


def calculate_coupon_discount(
    *,
    coupon: Coupon,
    amount,
):
    """
    محاسبه مبلغ تخفیف کوپن

    amount:
        مبلغ قابل پرداخت
    """

    amount = Decimal(str(amount))

    if amount <= 0:
        return Decimal("0")

    discount = coupon.discount

    if discount.discount_type == discount.PERCENT:

        return (
            amount *
            discount.value
        ) / Decimal("100")

    if discount.discount_type == discount.FIXED:

        return min(
            Decimal(str(discount.value)),
            amount,
        )

    return Decimal("0")


@transaction.atomic
def register_coupon_usage(
    *,
    coupon: Coupon,
    user,
    order,
):
    """
    ثبت استفاده از کوپن
    """

    CouponUsage.objects.create(
        coupon=coupon,
        user=user,
        order=order,
    )

    coupon.used_count += 1

    coupon.save(
        update_fields=[
            "used_count",
        ]
    )

    return coupon