from django.test import TestCase

from checkout.services import (
    prepare_checkout,
    confirm_checkout,
)

from carts.tests.factories import create_cart
from addresses.tests.factories import address_factory
from shipping.tests.factories import create_shipping_method
from discounts.tests.factories import create_coupon
from orders.tests.factories import (
    create_order,
    create_user,
)
from payments.tests.factories import create_payment


class PrepareCheckoutTests(TestCase):

    def setUp(self):
        self.user = create_user()

        self.cart = create_cart(
            user=self.user,
        )

        self.address = address_factory(
            user=self.user,
            is_default=True,
        )

        self.shipping_method = create_shipping_method(
            price=50000,
        )

    def test_prepare_checkout_default(self):
        result = prepare_checkout(
            user=self.user,
        )

        self.assertEqual(result["cart"], self.cart)
        self.assertEqual(result["address"], self.address)
        self.assertEqual(result["shipping_method"], self.shipping_method)
        self.assertEqual(result["shipping_cost"], self.shipping_method.price)
        self.assertIsNone(result["coupon"])

    def test_prepare_checkout_change_address(self):
        new_address = address_factory(
            user=self.user,
        )

        result = prepare_checkout(
            user=self.user,
            address_id=new_address.id,
        )

        new_address.refresh_from_db()
        self.address.refresh_from_db()

        self.assertTrue(new_address.is_default)
        self.assertFalse(self.address.is_default)
        self.assertEqual(result["address"], new_address)

    def test_prepare_checkout_change_shipping_method(self):
        second_shipping_method = create_shipping_method(
            price=70000,
        )

        result = prepare_checkout(
            user=self.user,
            shipping_method_id=second_shipping_method.id,
        )

        self.assertEqual(
            result["shipping_method"],
            second_shipping_method,
        )

        self.assertEqual(
            result["shipping_cost"],
            second_shipping_method.price,
        )

    def test_prepare_checkout_with_coupon(self):
        coupon = create_coupon()

        result = prepare_checkout(
            user=self.user,
            coupon_code=coupon.code,
        )

        self.assertEqual(
            result["coupon"],
            coupon,
        )

    def test_prepare_checkout_without_coupon(self):
        result = prepare_checkout(
            user=self.user,
        )

        self.assertIsNone(
            result["coupon"],
        )

    def test_prepare_checkout_without_address(self):
        self.address.delete()

        result = prepare_checkout(
            user=self.user,
        )

        self.assertIsNone(result["address"])