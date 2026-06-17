from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from orders.tests.factories import create_order, create_user

from payments.constants import (
    GatewayType,
    PaymentStatus,
)
from payments.services.payment import (
    create_payment,
    mark_payment_failed,
    mark_payment_success,
    verify_payment,
)
from shipping.tests.factories import create_shipping_method

from .factories import create_payment as create_payment_factory




class PaymentServicesTestCase(TestCase):
    def setUp(self):
        self.user = create_user()
        self.shipping_method = create_shipping_method()

        self.order = create_order(
            shipping_method=self.shipping_method,
            user=self.user,
        )

    @patch(
        "payments.services.payment.get_gateway"
    )
    def test_create_payment(
        self,
        mock_get_gateway,
    ):
        """
        باید پرداخت جدید ایجاد شود.
        """

        mock_gateway = mock_get_gateway.return_value

        mock_gateway.request_payment.return_value = {
            "authority": "AUTH-123",
            "payment_url": (
                "https://example.com/pay"
            ),
        }

        result = create_payment(
            order=self.order,
            gateway_type=GatewayType.ZARINPAL,
            callback_url="https://example.com/callback",
        )

        payment = result["payment"]

        self.assertEqual(
            payment.order,
            self.order,
        )

        self.assertEqual(
            payment.authority,
            "AUTH-123",
        )

        self.assertEqual(
            payment.status,
            PaymentStatus.PENDING,
        )

        self.assertEqual(
            result["payment_url"],
            "https://example.com/pay",
        )


    def test_create_payment_for_paid_order(self):
        """
        برای سفارش پرداخت شده نباید
        پرداخت جدید ایجاد شود.
        """

        self.order.paid_at = timezone.now()

        self.order.save()

        with self.assertRaises(
            ValidationError,
        ):
            create_payment(
                order=self.order,
                gateway_type=GatewayType.ZARINPAL,
                callback_url="https://example.com",
            )

    def test_mark_payment_failed(self):
        """
        باید پرداخت را Failed کند.
        """

        payment = create_payment_factory(
            order=self.order,
        )

        mark_payment_failed(
            payment,
            "Gateway Error",
        )

        payment.refresh_from_db()

        self.assertEqual(
            payment.status,
            PaymentStatus.FAILED,
        )

        self.assertEqual(
            payment.failure_reason,
            "Gateway Error",
        )

    def test_mark_payment_success(self):
        """
        باید پرداخت را Success کند.
        """

        payment = create_payment_factory(
            order=self.order,
        )

        mark_payment_success(
            payment=payment,
            ref_id="123456",
        )

        payment.refresh_from_db()
        self.order.refresh_from_db()

        self.assertEqual(
            payment.status,
            PaymentStatus.SUCCESS,
        )

        self.assertEqual(
            payment.ref_id,
            "123456",
        )

        self.assertIsNotNone(
            payment.paid_at,
        )

        self.assertIsNotNone(
            self.order.paid_at,
        )


    @patch(
        "payments.services.payment.get_gateway"
    )
    def test_verify_payment(
        self,
        mock_get_gateway,
    ):
        """
        باید پرداخت را تایید کند.
        """

        payment = create_payment_factory(
            order=self.order,
            authority="AUTH-123",
        )

        mock_gateway = (
            mock_get_gateway.return_value
        )

        mock_gateway.verify_payment.return_value = {
            "success": True,
            "ref_id": "987654",
        }

        result = verify_payment(
            authority="AUTH-123",
        )

        result.refresh_from_db()

        self.assertEqual(
            result.status,
            PaymentStatus.SUCCESS,
        )

        self.assertEqual(
            result.ref_id,
            "987654",
        )


    def test_verify_payment_not_found(self):
        """
        اگر پرداخت وجود نداشته باشد
        باید خطا بدهد.
        """

        with self.assertRaises(
            ValidationError,
        ):
            verify_payment(
                authority="INVALID",
            )

    # بعد اضافه کردن state service دیگر نیاز نیست
    # def test_verify_payment_not_pending(self):
    #     """
    #     فقط پرداخت Pending
    #     قابل Verify است.
    #     """
    #
    #     payment = create_payment_factory(
    #         order=self.order,
    #         authority="AUTH-123",
    #         status=PaymentStatus.SUCCESS,
    #     )
    #
    #     with self.assertRaises(
    #         ValidationError,
    #     ):
    #         verify_payment(
    #             authority=payment.authority,
    #         )


    @patch("payments.services.payment.get_gateway")
    def test_verify_payment_sets_order_paid_at(
            self,
            mock_get_gateway,
    ):
        """
        بعد از پرداخت موفق باید paid_at سفارش ثبت شود.
        """

        payment = create_payment_factory(
            order=self.order,
            gateway_type="ZARINPAL",
            callback_url="http://test/callback/",
        )

        mock_gateway = mock_get_gateway.return_value
        mock_gateway.verify_payment.return_value = {
            "success": True,
            "ref_id": "REF-123",
        }

        verify_payment(
            authority=payment.authority,
        )

        payment.order.refresh_from_db()

        self.assertIsNotNone(
            payment.order.paid_at,
        )


    @patch("payments.services.payment.get_gateway")
    def test_verify_payment_is_idempotent(
            self,
            mock_get_gateway,
    ):
        """
        Callback نباید دوبار اثر مخرب داشته باشد.
        """

        payment = create_payment_factory(
            order=self.order,
            gateway_type="ZARINPAL",
            callback_url="http://test/callback/",
        )

        mock_gateway = mock_get_gateway.return_value
        mock_gateway.verify_payment.return_value = {
            "success": True,
            "ref_id": "REF-123",
        }

        verify_payment(
            authority=payment.authority,
        )

        payment.refresh_from_db()
        first_paid_at = payment.order.paid_at

        verify_payment(
            authority=payment.authority,
        )

        payment.refresh_from_db()

        self.assertEqual(
            payment.status,
            PaymentStatus.SUCCESS,
        )

        self.assertEqual(
            payment.ref_id,
            "REF-123",
        )

        self.assertEqual(
            payment.order.paid_at,
            first_paid_at,
        )

