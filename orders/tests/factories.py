from django.contrib.auth import get_user_model

from orders.constants import OrderStatus
from orders.models import Order, OrderItem
from orders.services.order_number import generate_order_number


User = get_user_model()


def create_user(**kwargs):
    return User.objects.create_user(
        phone_number=kwargs.get("phone_number", "09120000000"),
        password="testpass123",
    )


def create_order(user, **kwargs):
    return Order.objects.create(
        user=user,
        order_number=kwargs.get("order_number", generate_order_number()),
        status=kwargs.get("status", OrderStatus.PENDING),
        address_snapshot=kwargs.get("address_snapshot", {}),
        subtotal=kwargs.get("subtotal", 100000),
        discount_amount=kwargs.get("discount_amount", 0),
        shipping_cost=kwargs.get("shipping_cost", 0),
        total_amount=kwargs.get("total_amount", 100000),
    )