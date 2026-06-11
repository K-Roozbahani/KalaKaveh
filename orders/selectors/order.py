from django.db.models import Prefetch

from orders.models import Order, OrderItem
from orders.constants import OrderStatus


def get_order_queryset():
    """
    Base queryset for all order selectors.
    """

    return (
        Order.objects
        .select_related("user")
        .prefetch_related(
            Prefetch(
                "items",
                queryset=OrderItem.objects.select_related(
                    "product",
                    "variant",
                ),
            )
        )
    )


def get_order_by_id(order_id: int):
    """
    Get order by id.
    """

    return (
        get_order_queryset()
        .filter(id=order_id)
        .first()
    )


def get_order_by_number(order_number: str):
    """
    Get order by order_number.
    """

    return (
        get_order_queryset()
        .filter(order_number=order_number)
        .first()
    )


def get_user_orders(user):
    """
    All user orders.
    """

    return (
        get_order_queryset()
        .filter(user=user)
    )


def get_user_order_by_id(user, order_id: int):
    """
    Single user order.
    """

    return (
        get_order_queryset()
        .filter(
            user=user,
            id=order_id,
        )
        .first()
    )


def get_user_order_by_number(user, order_number: str):
    """
    Single user order by order number.
    """

    return (
        get_order_queryset()
        .filter(
            user=user,
            order_number=order_number,
        )
        .first()
    )


def get_user_pending_orders(user):
    """
    Pending orders.
    """

    return (
        get_order_queryset()
        .filter(
            user=user,
            status=OrderStatus.PENDING,
        )
    )


def get_user_confirmed_orders(user):
    """
    Confirmed orders.
    """

    return (
        get_order_queryset()
        .filter(
            user=user,
            status=OrderStatus.CONFIRMED,
        )
    )


def get_user_processing_orders(user):
    """
    Processing orders.
    """

    return (
        get_order_queryset()
        .filter(
            user=user,
            status=OrderStatus.PROCESSING,
        )
    )


def get_user_completed_orders(user):
    """
    Completed orders.
    """

    return (
        get_order_queryset()
        .filter(
            user=user,
            status=OrderStatus.COMPLETED,
        )
    )


def get_user_canceled_orders(user):
    """
    Canceled orders.
    """

    return (
        get_order_queryset()
        .filter(
            user=user,
            status=OrderStatus.CANCELED,
        )
    )


def get_orders_by_status(status: str):
    """
    Admin selector.
    """

    return (
        get_order_queryset()
        .filter(status=status)
    )


def get_recent_orders(limit: int = 10):
    """
    Recent orders.
    """

    return (
        get_order_queryset()
        .order_by("-created_at")[:limit]
    )


def get_order_items(order):
    """
    Order items.
    """

    return (
        order.items
        .select_related(
            "product",
            "variant",
        )
        .all()
    )