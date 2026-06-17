from orders.tests.factories import create_order
from shipping.constants import ShipmentStatus
from shipping.models import (
    Shipment,
    ShippingMethod,
)


def create_shipping_method(**kwargs):
    return ShippingMethod.objects.create(
        name=kwargs.get(
            "name",
            "پست پیشتاز",
        ),
        code=kwargs.get(
            "code",
            f"POST-{ShippingMethod.objects.count() + 1}",
        ),
        price=kwargs.get(
            "price",
            50000,
        ),
        estimated_days=kwargs.get(
            "estimated_days",
            3,
        ),
        is_active=kwargs.get(
            "is_active",
            True,
        ),
    )


def create_shipment(order=None, **kwargs):
    if order is None:
        order = create_order()
    shipping_method = kwargs.get(
        "shipping_method",
    )

    if shipping_method is None:
        shipping_method = (
            create_shipping_method()
        )

    return Shipment.objects.create(
        order=order,
        shipping_method=shipping_method,
        tracking_code=kwargs.get(
            "tracking_code",
            "",
        ),
        status=kwargs.get(
            "status",
            ShipmentStatus.PENDING,
        ),
        shipped_at=kwargs.get(
            "shipped_at",
            None,
        ),
        delivered_at=kwargs.get(
            "delivered_at",
            None,
        ),
        description=kwargs.get(
            "description",
            "",
        ),
    )