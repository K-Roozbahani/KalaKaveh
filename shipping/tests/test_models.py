from django.test import TestCase

from shipping.constants import ShipmentStatus

from shipping.tests.factories import (
    create_shipment,
    create_shipping_method,
)

from orders.tests.factories import (
    create_order, create_user
)


class ShippingMethodModelTest(TestCase):
    def test_create_shipping_method(self):
        shipping_method = create_shipping_method()

        self.assertEqual(
            shipping_method.name,
            "پست پیشتاز",
        )

        self.assertTrue(
            shipping_method.is_active,
        )

    def test_shipping_method_str(self):
        shipping_method = create_shipping_method(
            name="تیپاکس",
        )

        self.assertEqual(
            str(shipping_method),
            "تیپاکس",
        )


class ShipmentModelTest(TestCase):
    def test_create_shipment(self):
        user = create_user()
        order = create_order(user)

        shipment = create_shipment(
            order=order,
        )

        self.assertEqual(
            shipment.order,
            order,
        )

        self.assertEqual(
            shipment.status,
            ShipmentStatus.PENDING,
        )

    def test_default_status_is_pending(self):
        user = create_user()
        order = create_order(user)

        shipment = create_shipment(
            order=order,
        )

        self.assertEqual(
            shipment.status,
            ShipmentStatus.PENDING,
        )

    def test_tracking_code_default_is_empty(self):
        user = create_user()
        order = create_order(user)

        shipment = create_shipment(
            order=order,
        )

        self.assertEqual(
            shipment.tracking_code,
            "",
        )

    def test_shipped_at_default_is_none(self):
        user = create_user()
        order = create_order(user)

        shipment = create_shipment(
            order=order,
        )

        self.assertIsNone(
            shipment.shipped_at,
        )

    def test_delivered_at_default_is_none(self):
        user = create_user()
        order = create_order(user)

        shipment = create_shipment(
            order=order,
        )

        self.assertIsNone(
            shipment.delivered_at,
        )

    def test_description_default_is_empty(self):
        user = create_user()
        order = create_order(user)

        shipment = create_shipment(
            order=order,
        )

        self.assertEqual(
            shipment.description,
            "",
        )

    def test_shipment_str(self):
        user = create_user()
        order = create_order(user)

        shipment = create_shipment(
            order=order,
        )

        self.assertEqual(
            str(shipment),
            f"Shipment - {shipment.order.order_number}"
        )