from django.db import transaction

from orders.services.order import create_order_from_cart

from payments.services.payment import create_payment


@transaction.atomic
def start_checkout(
    *,
    user,
    address_id,
    shipping_method_id,
    gateway,
    callback_url,
    coupon=None,
    note="",
):
    """
    شروع فرآیند Checkout.

    Workflow:

        1- ایجاد سفارش از سبد خرید
        2- ایجاد رکورد پرداخت
        3- بازگرداندن Payment

    تمام Validationها و Business Ruleها داخل
    Serviceهای Orders و Payments انجام می‌شوند.
    """

    order = create_order_from_cart(
        user=user,
        address_id=address_id,
        shipping_method_id=shipping_method_id,
        coupon=coupon,
        note=note,
    )

    payment = create_payment(
        order=order,
        gateway_type=gateway,
        callback_url = callback_url,
    )

    return payment