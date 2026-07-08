from payments.constants import (
    GatewayType,
    PaymentStatus,
)
from payments.models import Payment


def create_payment(order, **kwargs):
    return Payment.objects.create(
        order=order,
        gateway=kwargs.get(
            "gateway",
            GatewayType.ZARINPAL,
        ),
        authority=kwargs.get(
            "authority",
            f"AUTH-{Payment.objects.count() + 1}",
        ),
        ref_id=kwargs.get(
            "ref_id",
            "",
        ),
        amount=kwargs.get(
            "amount",
            order.total_amount,
        ),
        status=kwargs.get(
            "status",
            PaymentStatus.PENDING,
        ),
        failure_reason=kwargs.get(
            "failure_reason",
            "",
        ),
        paid_at=kwargs.get(
            "paid_at",
            None,
        ),
    )