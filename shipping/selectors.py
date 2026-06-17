from shipping.models import (
    Shipment,
    ShippingMethod,
)


def get_shipping_method_queryset():
    return ShippingMethod.objects.all()


def get_shipping_method_by_id(
    shipping_method_id,
):
    return (
        get_shipping_method_queryset()
        .filter(
            id=shipping_method_id,
        )
        .first()
    )


def get_active_shipping_methods():
    return (
        get_shipping_method_queryset()
        .active()
    )


def get_shipment_queryset():
    return Shipment.objects.select_related(
        "order",
        "shipping_method",
    )


def get_shipment_by_id(
    shipment_id,
):
    return (
        get_shipment_queryset()
        .filter(
            id=shipment_id,
        )
        .first()
    )


def get_order_shipment(
    order,
):
    return (
        get_shipment_queryset()
        .filter(
            order=order,
        )
        .first()
    )