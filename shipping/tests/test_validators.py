from django.core.exceptions import ValidationError
from django.test import TestCase

from orders.tests.factories import create_order, create_user
from shipping.tests.factories import (
    create_shipment,
    create_shipping_method,
)

from shipping.validators import (
    validate_shipping_method_active,
    validate_shipping_method_exists,
    validate_shipment_exists,
)


class ValidateShippingMethodExistsTest(TestCase):
    def test_validate_shipping_method_exists_success(self):
        shipping_method = create_shipping_method()

        validate_shipping_method_exists(
            shipping_method,
        )

    def test_validate_shipping_method_exists_failed(self):
        with self.assertRaises(
            ValidationError,
        ):
            validate_shipping_method_exists(
                None,
            )


class ValidateShippingMethodActiveTest(TestCase):
    def setUp(self):
        self.user = create_user()
        self.shipping_method = create_shipping_method()

        self.order = create_order(
            shipping_method=self.shipping_method,
            user=self.user,
        )

    def test_validate_shipping_method_active_success(self):
        shipping_method = create_shipping_method(
            is_active=True,
        )

        validate_shipping_method_active(
            shipping_method,
        )

    def test_validate_shipping_method_active_failed(self):
        shipping_method = create_shipping_method(
            is_active=False,
        )

        with self.assertRaises(
            ValidationError,
        ):
            validate_shipping_method_active(
                shipping_method,
            )


class ValidateShipmentExistsTest(TestCase):
    def test_validate_shipment_exists_success(self):
        user = create_user()
        shipping_method = create_shipping_method()
        order = create_order(
            shipping_method=shipping_method,
            user=user,
        )
        shipment = create_shipment(order=order)

        validate_shipment_exists(
            shipment,
        )

    def test_validate_shipment_exists_failed(self):
        with self.assertRaises(
            ValidationError,
        ):
            validate_shipment_exists(
                None,
            )