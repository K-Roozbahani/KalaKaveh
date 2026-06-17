from django.test import TestCase

from orders.tests.factories import create_user, create_order
from orders.selectors import (
    get_user_orders,
    get_user_order_by_number,
)
from shipping.tests.factories import create_shipping_method


class OrderSelectorTest(TestCase):

    def setUp(self):
        self.user = create_user()
        self.shipping_method = create_shipping_method()
        self.order = create_order(
            user=self.user,
            shipping_method=self.shipping_method,
        )

    def test_get_user_orders(self):
        qs = get_user_orders(self.user)
        self.assertEqual(qs.count(), 1)

    def test_get_order_by_number(self):
        order = get_user_order_by_number(
            self.user,
            self.order.order_number,
        )
        self.assertIsNotNone(order)