from django.test import TestCase

from orders.constants import OrderStatus
from orders.tests.factories import create_user, create_order


class OrderModelTest(TestCase):

    def setUp(self):
        self.user = create_user()

    def test_order_creation(self):
        order = create_order(self.user)

        self.assertEqual(order.user, self.user)
        self.assertTrue(order.order_number.startswith("ORD"))
        self.assertEqual(order.status, OrderStatus.PENDING)