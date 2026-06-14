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

from .validators import (
    validate_payment_exists,
    validate_order_not_paid,
    validate_payment_is_pending,
)


def create_payment(*, order, gateway: str) -> Payment:
    """
    ایجاد پرداخت برای سفارش
    """

    # بررسی اینکه سفارش قبلاً پرداخت نشده باشد
    validate_order_not_paid(order)

    payment = Payment.objects.create(
        order=order,
        gateway=gateway,
        amount=order.total_amount,
        status=PaymentStatus.PENDING,
    )

    return payment


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


def verify_payment(*, authority: str, ref_id: str) -> Payment:
    """
    بررسی و تایید پرداخت از طریق authority
    """

    payment = get_payment_by_authority(authority)

    validate_payment_exists(payment)
    validate_payment_is_pending(payment)

    # اینجا در آینده gateway verify می‌شود
    return mark_payment_success(
        payment=payment,
        ref_id=ref_id,
    )


def get_payment_detail(payment_id: int) -> Payment:
    """
    دریافت جزئیات پرداخت
    """

    payment = get_payment_by_id(payment_id)

    validate_payment_exists(payment)

    return payment

