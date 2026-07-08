"""
Orchestrator مربوط به Callback درگاه پرداخت.

این سرویس فقط مسئول هماهنگی بین Payment و Order است و
هیچ Business Logic مستقلی در آن قرار ندارد.
"""

from payments.constants import PaymentStatus

from payments.services.payment import verify_payment
from orders.services.completion import complete_paid_order


def process_gateway_callback(*, authority: str):
    """
    پردازش Callback درگاه پرداخت.

    Workflow:

        Verify Payment
            ↓
        Complete Order
            ↓
        Return Payment
    """

    payment = verify_payment(
        authority=authority,
    )

    # در صورت عدم موفقیت پرداخت، نیازی به تکمیل سفارش نیست.
    if payment.status != PaymentStatus.SUCCESS:
        return payment

    complete_paid_order(
        order=payment.order,
        payment=payment,
    )

    return payment