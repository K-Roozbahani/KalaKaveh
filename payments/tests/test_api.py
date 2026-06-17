from unittest.mock import patch

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from orders.tests.factories import create_order, create_user

from payments.constants import (
    GatewayType,
    PaymentStatus,
)
from shipping.tests.factories import create_shipping_method

from .factories import create_payment



class PaymentAPITestCase(APITestCase):

    def setUp(self):
        self.user = create_user(
            phone_number="09120000001",
        )

        self.other_user = create_user(
            phone_number="09120000002",
        )

        self.client.force_authenticate(
            self.user,
        )

        self.shipping_method = create_shipping_method()

        self.order = create_order(
            shipping_method=self.shipping_method,
            user=self.user,
        )

    def test_get_payment_list(self):
        """
        کاربر باید فقط پرداخت‌های خودش را ببیند.
        """

        create_payment(
            order=self.order,
        )

        other_order = create_order(
            user = self.other_user,
            shipping_method=self.shipping_method
        )

        create_payment(
            order=other_order,
        )

        response = self.client.get(
            reverse("payments-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            1,
        )

        self.assertEqual(
            len(response.data["results"]),
            1,
        )

    def test_get_payment_detail(self):
        """
        مالک باید بتواند پرداخت خود را مشاهده کند.
        """

        payment = create_payment(
            order=self.order,
        )

        response = self.client.get(
            reverse(
                "payments-detail",
                kwargs={
                    "pk": payment.pk,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            payment.id,
        )

    def test_user_cannot_access_other_user_payment(
        self,
    ):
        """
        کاربر نباید به پرداخت دیگران دسترسی داشته باشد.
        """

        other_order = create_order(
            shipping_method=self.shipping_method,
            user=self.other_user,

        )

        payment = create_payment(
            order=other_order,
        )

        response = self.client.get(
            reverse(
                "payments-detail",
                kwargs={
                    "pk": payment.pk,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    @patch(
        "payments.services.payment.get_gateway"
    )
    def test_create_payment(
        self,
        mock_get_gateway,
    ):
        """
        ایجاد پرداخت جدید.
        """

        mock_gateway = (
            mock_get_gateway.return_value
        )

        mock_gateway.request_payment.return_value = {
            "authority": "AUTH-123",
            "payment_url": "https://pay.test",
        }

        response = self.client.post(
            reverse(
                "payments-list",
            ),
            {
                "order_number": (
                    self.order.order_number
                ),
                "gateway": (
                    GatewayType.ZARINPAL
                ),
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertIn(
            "payment_url",
            response.data,
        )

    def test_create_payment_invalid_order(
        self,
    ):
        """
        سفارش نامعتبر باید خطا بدهد.
        """

        response = self.client.post(
            reverse(
                "payments-list",
            ),
            {
                "order_number": (
                    "INVALID-ORDER"
                ),
                "gateway": (
                    GatewayType.ZARINPAL
                ),
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_create_payment_for_paid_order(
        self,
    ):
        """
        برای سفارش پرداخت شده
        نباید پرداخت جدید ایجاد شود.
        """

        from django.utils import timezone

        self.order.paid_at = (
            timezone.now()
        )

        self.order.save()

        response = self.client.post(
            reverse(
                "payments-list",
            ),
            {
                "order_number": (
                    self.order.order_number
                ),
                "gateway": (
                    GatewayType.ZARINPAL
                ),
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    @patch(
        "payments.services.payment.get_gateway"
    )
    def test_payment_callback_success(
        self,
        mock_get_gateway,
    ):
        """
        Callback موفق باید پرداخت را تایید کند.
        """

        payment = create_payment(
            order=self.order,
            authority="AUTH-123",
        )

        mock_gateway = (
            mock_get_gateway.return_value
        )

        mock_gateway.verify_payment.return_value = {
            "success": True,
            "ref_id": "REF-123",
        }

        response = self.client.get(
            reverse(
                "payment-callback",
            ),
            {
                "Authority": (
                    payment.authority
                ),
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        payment.refresh_from_db()

        self.assertEqual(
            payment.status,
            PaymentStatus.SUCCESS,
        )


    def test_payment_callback_invalid_authority(
        self,
    ):
        """
        authority نامعتبر باید خطا بدهد.
        """

        response = self.client.get(
            reverse(
                "payment-callback",
            ),
            {
                "Authority": (
                    "INVALID"
                ),
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )