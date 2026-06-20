from unittest.mock import patch

from rest_framework.test import APITestCase
from rest_framework import status

from orders.tests.factories import create_user, create_order
from shipping.models import ShippingMethod
from shipping.tests.factories import create_shipping_method


class OrderAPITest(APITestCase):

    def setUp(self):
        self.user = create_user()
        self.client.force_authenticate(self.user)
        self.shipping_method = create_shipping_method()
        self.order = create_order(
            shipping_method=self.shipping_method,
            user=self.user
        )

    def test_list_orders(self):
        response = self.client.get("/api/orders/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_retrieve_order(self):
        url = f"/api/orders/{self.order.order_number}/"

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    @patch("orders.api.views.create_order_from_cart")
    def test_create_order(self, mock_create):

        mock_create.return_value = self.order

        data = {
            "address_id": 1,
            "shipping_method_id": 1,
            "note": "test",
        }

        response = self.client.post(
            "/api/orders/",
            data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_order_items(self):

        url = f"/api/orders/{self.order.order_number}/items/"

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_latest_order(self):

        response = self.client.get(
            "/api/orders/latest/"
        )

        self.assertIn(
            response.status_code,
            [
                status.HTTP_200_OK,
                status.HTTP_204_NO_CONTENT,
            ],
        )

