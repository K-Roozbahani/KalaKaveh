from django.core.exceptions import ValidationError

from django.utils.translation import (
    gettext_lazy as _,
)

from shipping.constants import (
    ShipmentStatus,
)


ALLOWED_TRANSITIONS = {
    ShipmentStatus.PENDING: {
        ShipmentStatus.PACKAGED,
    },
    ShipmentStatus.PACKAGED: {
        ShipmentStatus.SHIPPED,
        ShipmentStatus.CANCELED,
    },
    ShipmentStatus.SHIPPED: {
        ShipmentStatus.DELIVERED,
        ShipmentStatus.RETURNED,
    },
    ShipmentStatus.DELIVERED: set(),
    ShipmentStatus.RETURNED: set(),
    ShipmentStatus.CANCELED: set(),
}


def can_transition(
    current_status,
    new_status,
):
    return (
        new_status
        in ALLOWED_TRANSITIONS.get(
            current_status,
            set(),
        )
    )


def transition_status(
    shipment,
    new_status,
):
    if not can_transition(
        shipment.status,
        new_status,
    ):
        raise ValidationError(
            _(
                "تغییر وضعیت مرسوله مجاز نیست."
            )
        )

    shipment.status = new_status

    shipment.save(
        update_fields=["status"],
    )

    return shipment