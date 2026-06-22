from decimal import Decimal


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