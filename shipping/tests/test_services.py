from django.core.exceptions import ValidationError
from django.test import TestCase

from shipping.constants import (
    ShipmentStatus,
)

from shipping.services import (
    assign_tracking_code,
    change_shipment_status,
    create_shipment_for_order,
    mark_as_delivered,
    mark_as_shipped,
)

from shipping.tests.factories import (
    create_shipment,
    create_shipping_method,
)

from orders.tests.factories import (
    create_order, create_user,
)


class CreateShipmentForOrderTest(TestCase):
    def test_create_shipment_for_order(self):
        user=create_user()
        shipping_method = create_shipping_method()
        order = create_order(
            user=user,
            shipping_method=shipping_method,
        )

        shipping_method = (
            create_shipping_method()
        )

        shipment = create_shipment_for_order(
            order=order,
            shipping_method=shipping_method,
        )

        self.assertEqual(
            shipment.order,
            order,
        )

        self.assertEqual(
            shipment.shipping_method,
            shipping_method,
        )

        self.assertEqual(
            shipment.status,
            ShipmentStatus.PENDING,
        )

    def test_create_shipment_for_order_returns_existing_shipment(
        self,
    ):
        shipping_method = create_shipping_method()
        order = create_order(
            shipping_method=shipping_method,
        )

        shipping_method = (
            create_shipping_method()
        )

        shipment = create_shipment(
            order=order,
            shipping_method=shipping_method,
        )

        result = create_shipment_for_order(
            order=order,
            shipping_method=shipping_method,
        )

        self.assertEqual(
            result,
            shipment,
        )

    def test_create_shipment_for_order_with_inactive_shipping_method(
        self,
    ):
        shipping_method = create_shipping_method()
        order = create_order(
            shipping_method=shipping_method,
        )

        shipping_method = (
            create_shipping_method(
                is_active=False,
            )
        )

        with self.assertRaises(
            ValidationError,
        ):
            create_shipment_for_order(
                order=order,
                shipping_method=shipping_method,
            )


class ChangeShipmentStatusTest(TestCase):
    def setUp(self):
        self.user = create_user()
        self.shipping_method = create_shipping_method()
        self.order = create_order(
            shipping_method=self.shipping_method,
            user=self.user,
        )

    def test_change_shipment_status(self):
        shipment = create_shipment(
            order=self.order,
            status=ShipmentStatus.PENDING,
        )

        shipment = change_shipment_status(
            shipment=shipment,
            new_status=ShipmentStatus.PACKAGED,
        )

        self.assertEqual(
            shipment.status,
            ShipmentStatus.PACKAGED,
        )

    def test_change_shipment_status_invalid_transition(
        self,
    ):

        shipment = create_shipment(
            order=self.order,
            status=ShipmentStatus.PENDING,
        )

        with self.assertRaises(
            ValidationError,
        ):
            change_shipment_status(
                shipment=shipment,
                new_status=ShipmentStatus.DELIVERED,
            )


class AssignTrackingCodeTest(TestCase):
    def test_assign_tracking_code(self):
        user = create_user()
        shipping_method = create_shipping_method()
        order = create_order(
            shipping_method=shipping_method,
            user=user,
        )
        shipment = create_shipment(
            order=order,
        )

        shipment = assign_tracking_code(
            shipment=shipment,
            tracking_code="TRK123456",
        )

        self.assertEqual(
            shipment.tracking_code,
            "TRK123456",
        )


class MarkAsShippedTest(TestCase):

    def setUp(self):
        self.user = create_user()
        self.shipping_method = create_shipping_method()
        self.order = create_order(
            user=self.user,
            shipping_method=self.shipping_method,
        )

    def test_mark_as_shipped(self):
        shipment = create_shipment(
            order=self.order,
            status=ShipmentStatus.PACKAGED,
        )

        shipment = mark_as_shipped(
            shipment=shipment,
        )

        self.assertEqual(
            shipment.status,
            ShipmentStatus.SHIPPED,
        )

        self.assertIsNotNone(
            shipment.shipped_at,
        )

    def test_mark_as_shipped_with_tracking_code(
        self,
    ):
        shipment = create_shipment(
            order=self.order,
            status=ShipmentStatus.PACKAGED,
        )

        shipment = mark_as_shipped(
            shipment=shipment,
            tracking_code="TRK999",
        )

        self.assertEqual(
            shipment.status,
            ShipmentStatus.SHIPPED,
        )

        self.assertEqual(
            shipment.tracking_code,
            "TRK999",
        )

        self.assertIsNotNone(
            shipment.shipped_at,
        )


class MarkAsDeliveredTest(TestCase):

    def setUp(self):
        self.user = create_user()
        self.shipping_method = create_shipping_method()
        self.order = create_order(
            user=self.user,
            shipping_method=self.shipping_method,
        )

    def test_mark_as_delivered(self):
        shipment = create_shipment(
            order=self.order,
            status=ShipmentStatus.SHIPPED,
        )

        shipment = mark_as_delivered(
            shipment=shipment,
        )

        self.assertEqual(
            shipment.status,
            ShipmentStatus.DELIVERED,
        )

        self.assertIsNotNone(
            shipment.delivered_at,
        )

    def test_mark_as_delivered_invalid_transition(
        self,
    ):
        shipment = create_shipment(
            order=self.order,
            status=ShipmentStatus.PENDING,
        )

        with self.assertRaises(
            ValidationError,
        ):
            mark_as_delivered(
                shipment=shipment,
            )