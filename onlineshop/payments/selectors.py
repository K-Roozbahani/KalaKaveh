from payments.models import Payment


def get_payment_queryset():
    """
    دریافت QuerySet پایه پرداخت‌ها.
    """

    return Payment.objects.select_related(
        "order",
        "order__user",
    )


def get_payment_by_id(payment_id):
    """
    دریافت پرداخت بر اساس شناسه.
    """

    return get_payment_queryset().filter(
        pk=payment_id,
    ).first()


def get_payment_by_authority(authority):
    """
    دریافت پرداخت بر اساس کد Authority.
    """

    return get_payment_queryset().filter(
        authority=authority,
    ).first()


def get_order_payments(order):
    """
    دریافت تمام پرداخت‌های یک سفارش.
    """

    return get_payment_queryset().filter(
        order=order,
    )


def get_user_payments(user):
    """
    دریافت تمام پرداخت‌های یک کاربر.
    """

    return get_payment_queryset().filter(
        order__user=user,
    )