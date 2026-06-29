from decimal import Decimal

from discounts.models import Coupon
from discounts.services.coupons import calculate_coupon_discount
from discounts.services.price_engine import calculate_variant_price


def calculate_cart_totals(
    *,
    cart,
    coupon: Coupon | None = None,
) -> dict:
    """
    محاسبه خلاصه مالی سبد خرید.

    این سرویس هیچ تغییری در دیتابیس ایجاد نمی‌کند و
    فقط وضعیت فعلی سبد خرید را محاسبه می‌کند.

    اگر Coupon ارسال شود، صرفاً مبلغ قابل پرداخت را
    شبیه‌سازی می‌کند و هیچ استفاده‌ای از کوپن ثبت
    نخواهد شد.
    """

    items_count = 0

    subtotal = Decimal("0")
    product_discount = Decimal("0")

    for item in cart.items.select_related("variant"):

        quantity = item.quantity

        pricing = calculate_variant_price(
            variant=item.variant,
        )

        items_count += quantity

        subtotal += (
            Decimal(pricing.base_price)
            * quantity
        )

        product_discount += (
            Decimal(pricing.discount_amount)
            * quantity
        )

    payable_amount = (
        subtotal -
        product_discount
    )

    coupon_discount = Decimal("0")

    if coupon is not None:

        coupon_discount = calculate_coupon_discount(
            coupon=coupon,
            amount=payable_amount,
        )

    total = max(
        payable_amount - coupon_discount,
        Decimal("0"),
    )

    return {
        "items_count": items_count,
        "subtotal": subtotal,
        "product_discount": product_discount,
        "coupon_discount": coupon_discount,
        "discount": (
            product_discount +
            coupon_discount
        ),
        "total": total,
    }