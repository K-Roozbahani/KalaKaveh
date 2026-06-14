from django.utils import timezone

from payments.models import Payment
from payments.constants import (
    PaymentStatus,
    GatewayType,
)

from payments.selectors import (
    get_payment_by_authority,
    get_payment_by_id,
)
from .gateways import get_gateway
from .state import transition_status

from .validators import (
    validate_payment_exists,
    validate_order_not_paid,
)


def create_payment(
    *,
    order,
    gateway_type,
    callback_url,
):
    """
    ایجاد پرداخت جدید.
    """

    validate_order_not_paid(order)

    payment = Payment.objects.create(
        order=order,
        gateway=gateway_type,
        amount=order.total_amount,
    )

    gateway = get_gateway(
        gateway_type,
    )

    response = gateway.request_payment(
        amount=payment.amount,
        description=f"Order {order.order_number}",
        callback_url=callback_url,
    )

    payment.authority = response["authority"]

    payment.save(
        update_fields=[
            "authority",
        ]
    )

    return {
        "payment": payment,
        "payment_url": response["payment_url"],
    }


def mark_payment_failed(payment: Payment, reason: str = "") -> Payment:
    """
    ثبت پرداخت ناموفق
    """

    payment.status = PaymentStatus.FAILED
    payment.failure_reason = reason
    payment.save(update_fields=[
        "status",
        "failure_reason",
    ])

    return payment


def mark_payment_success(payment: Payment, ref_id: str) -> Payment:
    """
    ثبت پرداخت موفق
    """

    payment.status = PaymentStatus.SUCCESS
    payment.ref_id = ref_id
    payment.paid_at = timezone.now()
    payment.save(update_fields=[
        "status",
        "ref_id",
        "paid_at",
    ])

    # آپدیت Order
    order = payment.order
    order.paid_at = payment.paid_at
    order.save(update_fields=["paid_at"])

    return payment



def verify_payment(*, authority):
    payment = get_payment_by_authority(authority)

    validate_payment_exists(payment)

    # ✅ idempotency built-in
    if payment.status == PaymentStatus.SUCCESS:
        return payment

    gateway = get_gateway(payment.gateway)

    result = gateway.verify_payment(
        authority=authority,
        amount=payment.amount,
    )

    if not result["success"]:
        transition_status(
            payment,
            PaymentStatus.FAILED,
        )
        return payment

    transition_status(
        payment,
        PaymentStatus.SUCCESS,
    )

    payment.ref_id = result["ref_id"]
    payment.paid_at = (
        payment.paid_at or timezone.now()
    )

    payment.save(
        update_fields=[
            "ref_id",
            "paid_at",
        ]
    )

    order = payment.order

    if order.paid_at is None:
        order.paid_at = timezone.now()
        order.save(update_fields=["paid_at"])

    return payment

def get_payment_detail(payment_id: int) -> Payment:
    """
    دریافت جزئیات پرداخت
    """

    payment = get_payment_by_id(payment_id)

    validate_payment_exists(payment)

    return payment

