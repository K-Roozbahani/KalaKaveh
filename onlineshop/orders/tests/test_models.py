from django.test import TestCase

from orders.constants import OrderStatus
from orders.tests.factories import create_user, create_order
from shipping.tests.factories import create_shipping_method


class OrderModelTest(TestCase):

    def setUp(self):
        self.user = create_user()
        self.shipping_method = create_shipping_method()
    def test_order_creation(self):
        order = create_order(
            shipping_method=self.shipping_method,
            user=self.user,
        )

        self.assertEqual(order.user, self.user)
        self.assertTrue(order.order_number.startswith("ORD"))
        self.assertEqual(order.status, OrderStatus.PENDING)