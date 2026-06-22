from decimal import Decimal

from discounts.services.discount import (
    calculate_variant_price,
)

from discounts.services.coupon import (
    calculate_coupon_discount,
)


def calculate_cart_totals(*, cart):
    """
    محاسبه کامل قیمت سبد خرید (Single Source of Truth)
    """

    items_count = 0
    subtotal = Decimal("0")
    product_discount = Decimal("0")

    for item in cart.items.select_related("variant").all():

        variant = item.variant
        quantity = item.quantity

        items_count += quantity

        pricing = calculate_variant_price(
            variant=variant,
        )

        subtotal += Decimal(str(pricing["price"])) * quantity

        product_discount += (
            Decimal(str(pricing["discount_amount"])) * quantity
        )

    coupon_discount = Decimal("0")

    if getattr(cart, "coupon", None):

        coupon_discount = calculate_coupon_discount(
            coupon=cart.coupon,
            amount=(subtotal - product_discount),
        )

    total = subtotal - product_discount - coupon_discount

    if total < 0:
        total = Decimal("0")

    return {
        "items_count": items_count,
        "subtotal": subtotal,
        "product_discount": product_discount,
        "coupon_discount": coupon_discount,
        "discount": product_discount + coupon_discount,
        "total": total,
    }