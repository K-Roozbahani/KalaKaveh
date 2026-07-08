from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from orders.tests.factories import create_user


class CheckoutViewTests(APITestCase):

    def setUp(self):
        self.user = create_user()
        self.url = reverse("checkout:checkout-list")
        self.confirm_url = reverse("checkout:checkout-confirm")

    def test_checkout_requires_authentication(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    @patch("checkout.api.views.prepare_checkout")
    def test_checkout_update(
            self,
            mock_prepare_checkout,
    ):
        self.client.force_authenticate(self.user)

        mock_prepare_checkout.return_value = {}

        response = self.client.post(
            self.url,
            {
                "address_id": 1,
                "shipping_method_id": 2,
                "coupon_code": "OFF20",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        mock_prepare_checkout.assert_called_once_with(
            user=self.user,
            address_id=1,
            shipping_method_id=2,
            coupon_code="OFF20",
        )

    @patch("checkout.api.views.confirm_checkout")
    def test_checkout_confirm(
            self,
            mock_confirm_checkout,
    ):
        self.client.force_authenticate(self.user)

        payment = type(
            "Payment",
            (),
            {
                "payment_url": "https://gateway.test",
            },
        )

        mock_confirm_checkout.return_value = payment

        response = self.client.post(
            self.confirm_url,
            {
                "gateway_type": "zarinpal",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["payment_url"],
            "https://gateway.test",
        )

        self.assertEqual(
            mock_confirm_checkout.call_args.kwargs["user"],
            self.user,
        )

    def test_checkout_confirm_requires_authentication(self):
        response = self.client.post(
            self.confirm_url,
            {
                "gateway_type": "zarinpal",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

