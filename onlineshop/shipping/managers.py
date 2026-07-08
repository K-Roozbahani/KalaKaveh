from django.db import models

from shipping.constants import ShipmentStatus


class ShippingMethodQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class ShipmentQuerySet(models.QuerySet):
    def pending(self):
        return self.filter(
            status=ShipmentStatus.PENDING,
        )

    def packaged(self):
        return self.filter(
            status=ShipmentStatus.PACKAGED,
        )

    def shipped(self):
        return self.filter(
            status=ShipmentStatus.SHIPPED,
        )

    def delivered(self):
        return self.filter(
            status=ShipmentStatus.DELIVERED,
        )

    def returned(self):
        return self.filter(
            status=ShipmentStatus.RETURNED,
        )

    def canceled(self):
        return self.filter(
            status=ShipmentStatus.CANCELED,
        )