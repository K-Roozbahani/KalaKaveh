from django.db import transaction

from discounts.services.coupon import register_coupon_usage

from orders.models import Order
from orders.services.status import mark_order_confirmed

from payments.models import Payment


# =====================================================
# Order Completion
# =====================================================

@transaction.atomic
def complete_paid_order(
    order: Order,
    payment: Payment,
) -> Order:
    """
    تکمیل سفارش پس از پرداخت موفق

    مسئول هماهنگی عملیات پس از پرداخت موفق است.
    """

    # -------------------------------------------------
    # تغییر وضعیت سفارش
    # -------------------------------------------------

    mark_order_confirmed(order)

    # -------------------------------------------------
    # ثبت استفاده از کوپن
    # -------------------------------------------------

    if order.coupon_id:
        register_coupon_usage(
            coupon=order.coupon,
            user=order.user,
            order=order,
        )

    # -------------------------------------------------
    # Future Hooks
    # -------------------------------------------------

    # decrease_stock(...)
    # create_invoice(...)
    # send_sms(...)
    # send_email(...)
    # publish_event(...)

    return order