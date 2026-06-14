from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from payments.constants import PaymentStatus


def validate_payment_exists(payment):
    """
    بررسی وجود پرداخت.
    """

    if payment is None:
        raise ValidationError(
            _("پرداخت یافت نشد.")
        )


def validate_order_not_paid(order):
    """
    بررسی عدم پرداخت قبلی سفارش.
    """

    if order.paid_at is not None:
        raise ValidationError(
            _("این سفارش قبلاً پرداخت شده است.")
        )

# این متد به دلیل تداخل با سرویس پاک شد
# def validate_payment_is_pending(payment):
#     """
#     فقط پرداخت‌های در انتظار قابل Verify هستند.
#     """
#
#     if payment.status != PaymentStatus.PENDING:
#         raise ValidationError(
#             _("این پرداخت در وضعیت در انتظار نیست.")
#         )


def validate_payment_amount(
    payment_amount,
    gateway_amount,
):
    """
    بررسی تطابق مبلغ پرداخت با مبلغ بازگشتی درگاه.
    """

    if payment_amount != gateway_amount:
        raise ValidationError(
            _("مبلغ پرداخت معتبر نیست.")
        )


def validate_order_exists(order):
    if order is None:
        raise ValidationError(
            "سفارش یافت نشد."
        )