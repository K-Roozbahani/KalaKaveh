from django.test import TestCase

from orders.tests.factories import (
    create_order, create_user,
)

from shipping.selectors import (
    get_active_shipping_methods,
    get_order_shipment,
    get_shipment_by_id,
    get_shipment_queryset,
    get_shipping_method_by_id,
    get_shipping_method_queryset,
)

from shipping.tests.factories import (
    create_shipment,
    create_shipping_method,
)


class ShippingMethodSelectorTest(TestCase):
    def test_get_shipping_method_queryset(self):
        shipping_method = (
            create_shipping_method()
        )

        queryset = (
            get_shipping_method_queryset()
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first(),
            shipping_method,
        )

    def test_get_shipping_method_by_id(self):
        shipping_method = (
            create_shipping_method()
        )

        result = get_shipping_method_by_id(
            shipping_method.id,
        )

        self.assertEqual(
            result,
            shipping_method,
        )

    def test_get_shipping_method_by_id_not_found(self):
        result = get_shipping_method_by_id(
            99999,
        )

        self.assertIsNone(
            result,
        )

    def test_get_active_shipping_methods(self):
        active_method = (
            create_shipping_method(
                is_active=True,
            )
        )

        create_shipping_method(
            is_active=False,
        )

        queryset = (
            get_active_shipping_methods()
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first(),
            active_method,
        )


class ShipmentSelectorTest(TestCase):
    def setUp(self):
        self.user = create_user()
        self.shipping_method = create_shipping_method()
        self.order = create_order(
            user=self.user,
            shipping_method=self.shipping_method,
        )

    def test_get_shipment_queryset(self):
        shipment = create_shipment(
            order=self.order,
        )

        queryset = (
            get_shipment_queryset()
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertEqual(
            queryset.first(),
            shipment,
        )

    def test_get_shipment_by_id(self):
        shipment = create_shipment(
            order=self.order,
        )

        result = get_shipment_by_id(
            shipment.id,
        )

        self.assertEqual(
            result,
            shipment,
        )

    def test_get_shipment_by_id_not_found(self):
        result = get_shipment_by_id(
            99999,
        )

        self.assertIsNone(
            result,
        )

    def test_get_order_shipment(self):

        shipment = create_shipment(
            order=self.order,
        )

        result = get_order_shipment(
            order=self.order,
        )

        self.assertEqual(
            result,
            shipment,
        )

    def test_get_order_shipment_not_found(self):

        result = get_order_shipment(
            self.order,
        )

        self.assertIsNone(
            result,
        )