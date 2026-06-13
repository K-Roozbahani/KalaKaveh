from decimal import Decimal


def calculate_cart_totals(cart):
    """
    محاسبه خلاصه مالی سبد خرید

    خروجی:

    {
        "items_count": 3,
        "subtotal": 10000000,
        "discount": 500000,
        "coupon_discount": 100000,
        "total": 9400000,
    }
    """

    items_count = 0

    subtotal = Decimal("0")

    product_discount = Decimal("0")

    for item in cart.items.all():

        quantity = item.quantity

        variant = item.variant

        items_count += quantity

        subtotal += (
            variant.price *
            quantity
        )

        product_discount += (
            variant.discount_amount *
            quantity
        )

    coupon_discount = calculate_coupon_discount(
        cart=cart,
        subtotal=subtotal,
        product_discount=product_discount,
    )

    total = (
        subtotal
        - product_discount
        - coupon_discount
    )

    if total < 0:
        total = Decimal("0")

    return {
        "items_count": items_count,
        "subtotal": subtotal,

        # مجموع کل تخفیف
        "discount": (
                product_discount +
                coupon_discount
        ),

        # جزئیات تخفیف
        "product_discount": product_discount,
        "coupon_discount": coupon_discount,

        "total": total,
    }


def calculate_coupon_discount(
    *,
    cart,
    subtotal,
    product_discount,
):
    """
    محاسبه تخفیف ناشی از کوپن

    نکته:
    تخفیف کوپن روی مبلغ نهایی بعد از
    اعمال تخفیف محصولات محاسبه می‌شود.
    """

    coupon = cart.coupon

    if not coupon:
        return Decimal("0")

    payable_amount = (
        subtotal -
        product_discount
    )

    if payable_amount <= 0:
        return Decimal("0")

    if coupon.discount.discount_type == "percent":

        return (
            payable_amount *
            coupon.discount.value
        ) / Decimal("100")

    if coupon.discount.discount_type == "fixed":

        return min(
            Decimal(str(coupon.discount.value)),
            payable_amount,
        )

    return Decimal("0")