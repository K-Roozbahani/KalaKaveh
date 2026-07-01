from django.utils import timezone

from orders.models import Order
from orders.constants import OrderStatus


# =====================================================
# Order Status Machine
# =====================================================

_ALLOWED_TRANSITIONS = {
    OrderStatus.PENDING: {
        OrderStatus.CONFIRMED,
        OrderStatus.CANCELED,
    },
    OrderStatus.CONFIRMED: {
        OrderStatus.PROCESSING,
        OrderStatus.CANCELED,
    },
    OrderStatus.PROCESSING: {
        OrderStatus.COMPLETED,
        OrderStatus.CANCELED,
    },
    OrderStatus.COMPLETED: set(),
    OrderStatus.CANCELED: set(),
}


def can_change_status(order: Order, new_status: str) -> bool:
    """
    بررسی معتبر بودن تغییر وضعیت سفارش
    """

    return new_status in _ALLOWED_TRANSITIONS.get(order.status, set())


def change_order_status(order: Order, new_status: str) -> Order:
    """
    تغییر وضعیت سفارش
    """

    if not can_change_status(order, new_status):
        raise ValueError(
            f"Invalid order status transition: "
            f"{order.status} -> {new_status}"
        )

    update_fields = ["status"]

    order.status = new_status

    # ثبت زمان تکمیل سفارش
    # if new_status == OrderStatus.COMPLETED:
    #     order.paid_at = timezone.now()
    #     update_fields.append("paid_at")
    #
    # order.save(update_fields=update_fields)

    return order


# =====================================================
# Shortcut Methods
# =====================================================

def mark_order_confirmed(order: Order) -> Order:
    """
    تایید سفارش
    """
    change_order_status(
        order,
        OrderStatus.CONFIRMED,
    )

    if order.paid_at is None:
        order.paid_at = timezone.now()
        order.save(
            update_fields=[
                "paid_at",
            ]
        )

    return order


def mark_order_processing(order: Order) -> Order:
    """
    شروع آماده‌سازی سفارش
    """

    return change_order_status(
        order,
        OrderStatus.PROCESSING,
    )


def mark_order_completed(order: Order) -> Order:
    """
    تکمیل سفارش
    """

    return change_order_status(
        order,
        OrderStatus.COMPLETED,
    )


def mark_order_canceled(order: Order) -> Order:
    """
    لغو سفارش
    """

    return change_order_status(
        order,
        OrderStatus.CANCELED,
    )