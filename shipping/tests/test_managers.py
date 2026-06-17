from django.test import TestCase

from shipping.constants import ShipmentStatus

from shipping.models import (
    Shipment,
    ShippingMethod,
)

from shipping.tests.factories import (
    create_shipment,
    create_shipping_method,
)


class ShippingMethodQuerySetTest(TestCase):
    def test_active(self):
        active_method = create_shipping_method(
            is_active=True,
        )

        create_shipping_method(
            is_active=False,
        )

        queryset = ShippingMethod.objects.active()

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first(),
            active_method,
        )


class ShipmentQuerySetTest(TestCase):
    def test_pending(self):
        shipment = create_shipment(
            status=ShipmentStatus.PENDING,
        )

        create_shipment(
            status=ShipmentStatus.SHIPPED,
        )

        queryset = Shipment.objects.pending()

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first(),
            shipment,
        )

    def test_packaged(self):
        shipment = create_shipment(
            status=ShipmentStatus.PACKAGED,
        )

        create_shipment(
            status=ShipmentStatus.PENDING,
        )

        queryset = Shipment.objects.packaged()

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first(),
            shipment,
        )

    def test_shipped(self):
        shipment = create_shipment(
            status=ShipmentStatus.SHIPPED,
        )

        create_shipment(
            status=ShipmentStatus.PENDING,
        )

        queryset = Shipment.objects.shipped()

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first(),
            shipment,
        )

    def test_delivered(self):
        shipment = create_shipment(
            status=ShipmentStatus.DELIVERED,
        )

        create_shipment(
            status=ShipmentStatus.PENDING,
        )

        queryset = Shipment.objects.delivered()

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first(),
            shipment,
        )

    def test_returned(self):
        shipment = create_shipment(
            status=ShipmentStatus.RETURNED,
        )

        create_shipment(
            status=ShipmentStatus.PENDING,
        )

        queryset = Shipment.objects.returned()

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first(),
            shipment,
        )

    def test_canceled(self):
        shipment = create_shipment(
            status=ShipmentStatus.CANCELED,
        )

        create_shipment(
            status=ShipmentStatus.PENDING,
        )

        queryset = Shipment.objects.canceled()

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first(),
            shipment,
        )