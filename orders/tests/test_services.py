from django.test import TestCase
from unittest.mock import patch

from orders.tests.factories import create_user

from orders.services.order import create_order_from_cart


class OrderServiceTest(TestCase):

    def setUp(self):
        self.user = create_user()

    # @patch("orders.services.order.get_user_active_cart")
    # def test_create_order_from_cart_success(self, mock_cart):
    #     """
    #     Mock cart → simulate order creation
    #     """
    #
    #     class FakeVariant:
    #         id = 1
    #         price = 100000
    #         stock = 10
    #         product = type("P", (), {"id": 1, "name": "Test Product"})
    #
    #     class FakeItem:
    #         product = FakeVariant.product
    #         variant = FakeVariant()
    #         quantity = 1
    #
    #     class FakeCart:
    #         items = [FakeItem()]
    #         status = "active"
    #
    #     mock_cart.return_value = FakeCart()
    #
    #     with patch(
    #         "orders.services.order.get_address_by_id"
    #     ) as mock_address:
    #
    #         mock_address.return_value = type(
    #             "A",
    #             (),
    #             {
    #                 "user_id": self.user.id,
    #                 "receiver_name": "test",
    #                 "receiver_phone": "0912",
    #                 "province": type("P", (), {"name": "Tehran"}),
    #                 "city": type("C", (), {"name": "Tehran"}),
    #                 "address_line": "test",
    #                 "plaque": "1",
    #                 "unit": "1",
    #                 "postal_code": "1234567890",
    #                 "latitude": None,
    #                 "longitude": None,
    #             },
    #         )
    #
    #         order = create_order_from_cart(
    #             user=self.user,
    #             address_id=1,
    #             note="test note",
    #         )
    #
    #         self.assertIsNotNone(order)


