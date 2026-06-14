from payments.constants import PaymentStatus

ALLOWED_TRANSITIONS = {
    PaymentStatus.PENDING: [
        PaymentStatus.SUCCESS,
        PaymentStatus.FAILED,
    ],
    PaymentStatus.FAILED: [
        PaymentStatus.PENDING,  # retry
    ],
    PaymentStatus.SUCCESS: [
        # terminal state
    ],
    PaymentStatus.REFUNDED: [
        # terminal state
    ],
}


class InvalidPaymentStateTransition(Exception):
    pass


def can_transition(from_status, to_status):
    return to_status in ALLOWED_TRANSITIONS.get(from_status, [])


def transition_status(payment, new_status):
    if payment.status == new_status:
        return payment  # idempotent safe

    if not can_transition(payment.status, new_status):
        raise InvalidPaymentStateTransition(
            f"Cannot move from {payment.status} to {new_status}"
        )

    payment.status = new_status
    payment.save(update_fields=["status", "updated_at"])

    return payment


