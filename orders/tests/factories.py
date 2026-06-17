from django.contrib.auth import get_user_model

from orders.constants import OrderStatus
from orders.models import Order, OrderItem
from orders.services.order_number import generate_order_number


User = get_user_model()


def create_user(**kwargs):
    phone_number = kwargs.get(
        "phone_number"
    )

    if phone_number is None:
        phone_number = (
            f"091200000{User.objects.count() + 1:02d}"
        )

    return User.objects.create_user(
        phone_number=phone_number,
        password="testpass123",
    )


def create_shipping_snapshot():
    return {
        "id": 1,
        "name": "پست پیشتاز",
        "price": "80000",
        "estimated_days": 3,
    }



def create_order(user=None, **kwargs):
    if user is None:
        user = create_user()

    return Order.objects.create(
        user=user,
        order_number=kwargs.get(
            "order_number",
            generate_order_number(),
        ),
        status=kwargs.get(
            "status",
            OrderStatus.PENDING,
        ),
        address_snapshot=kwargs.get(
            "address_snapshot",
            {},
        ),
        shipping_method_snapshot=kwargs.get(
            "shipping_method_snapshot",
            create_shipping_snapshot(),
        ),
        subtotal=kwargs.get(
            "subtotal",
            100000,
        ),
        discount_amount=kwargs.get(
            "discount_amount",
            0,
        ),
        shipping_cost=kwargs.get(
            "shipping_cost",
            0,
        ),
        total_amount=kwargs.get(
            "total_amount",
            100000,
        ),
    )