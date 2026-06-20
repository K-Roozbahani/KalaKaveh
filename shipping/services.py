from django.db import transaction

from shipping.constants import ShipmentStatus

from shipping.selectors import (
    get_shipment_by_order,
    get_shipment_by_id,
)

from shipping.validators import (
    validate_shipping_method_active,
    validate_shipping_method_exists,
    validate_shipment_exists,
)

from shipping.state import (
    transition_status,
)

from shipping.models import (
    Shipment,
    ShippingMethod,
)


@transaction.atomic
def create_shipment_for_order(
    *,
    order,
    shipping_method,
    description="",
):
    validate_shipping_method_exists(
        shipping_method,
    )

    validate_shipping_method_active(
        shipping_method,
    )

    existing_shipment = get_shipment_by_order(
        order,
    )

    if existing_shipment:
        return existing_shipment

    shipment = Shipment.objects.create(
        order=order,
        shipping_method=shipping_method,
        status=ShipmentStatus.PENDING,
        description=description,
    )

    return shipment


@transaction.atomic
def create_shipment_for_order(
    *,
    order,
    shipping_method,
    description="",
):
    validate_shipping_method_exists(
        shipping_method,
    )

    validate_shipping_method_active(
        shipping_method,
    )

    existing_shipment = get_shipment_by_order(
        order,
    )

    if existing_shipment:
        return existing_shipment

    shipment = Shipment.objects.create(
        order=order,
        shipping_method=shipping_method,
        status=ShipmentStatus.PENDING,
        description=description,
    )

    return shipment


@transaction.atomic
def change_shipment_status(
    *,
    shipment,
    new_status,
):
    validate_shipment_exists(
        shipment,
    )

    return transition_status(
        shipment,
        new_status,
    )


@transaction.atomic
def assign_tracking_code(
    *,
    shipment,
    tracking_code,
):
    validate_shipment_exists(
        shipment,
    )

    shipment.tracking_code = tracking_code
    shipment.save(
        update_fields=["tracking_code"],
    )

    return shipment


from django.utils import timezone


@transaction.atomic
def mark_as_shipped(
    *,
    shipment,
    tracking_code=None,
):
    validate_shipment_exists(
        shipment,
    )

    if tracking_code:
        shipment.tracking_code = tracking_code

    shipment = transition_status(
        shipment,
        ShipmentStatus.SHIPPED,
    )

    shipment.shipped_at = timezone.now()

    shipment.save(
        update_fields=[
            "tracking_code",
            "shipped_at",
            "status",
        ],
    )

    return shipment


@transaction.atomic
def mark_as_delivered(
    *,
    shipment,
):
    validate_shipment_exists(
        shipment,
    )

    shipment = transition_status(
        shipment,
        ShipmentStatus.DELIVERED,
    )

    shipment.delivered_at = timezone.now()

    shipment.save(
        update_fields=[
            "delivered_at",
            "status",
        ],
    )

    return shipment


