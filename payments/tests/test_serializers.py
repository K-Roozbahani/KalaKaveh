from django.test import TestCase

from orders.tests.factories import create_order, create_user

from payments.constants import (
    GatewayType,
    PaymentStatus,
)
from payments.serializers import (
    PaymentCreateSerializer,
    PaymentDetailSerializer,
    PaymentListSerializer,
)

from .factories import create_payment


class PaymentCreateSerializerTestCase(TestCase):
    def test_serializer_valid_data(self):
        """
        باید داده معتبر را قبول کند.
        """

        serializer = PaymentCreateSerializer(
            data={
                "order_number": "ORD-123456",
                "gateway": GatewayType.ZARINPAL,
            }
        )

        self.assertTrue(
            serializer.is_valid()
        )

    def test_serializer_without_order_number(self):
        """
        شماره سفارش اجباری است.
        """

        serializer = PaymentCreateSerializer(
            data={
                "gateway": GatewayType.ZARINPAL,
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "order_number",
            serializer.errors,
        )

    def test_serializer_without_gateway(self):
        """
        درگاه پرداخت اجباری است.
        """

        serializer = PaymentCreateSerializer(
            data={
                "order_number": "ORD-123456",
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "gateway",
            serializer.errors,
        )

    def test_serializer_invalid_gateway(self):
        """
        درگاه نامعتبر نباید پذیرفته شود.
        """

        serializer = PaymentCreateSerializer(
            data={
                "order_number": "ORD-123456",
                "gateway": "invalid",
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "gateway",
            serializer.errors,
        )


class PaymentListSerializerTestCase(TestCase):
    def setUp(self):
        self.user = create_user()

        self.order = create_order(
            self.user,
        )

        self.payment = create_payment(
            order=self.order,
            amount=250000,
            status=PaymentStatus.PENDING,
        )

    def test_serializer_fields(self):
        """
        باید فیلدهای لیست پرداخت را برگرداند.
        """

        serializer = PaymentListSerializer(
            instance=self.payment,
        )

        data = serializer.data

        self.assertEqual(
            data["id"],
            self.payment.id,
        )

        self.assertEqual(
            data["order_number"],
            self.order.order_number,
        )

        self.assertEqual(
            data["gateway"],
            self.payment.gateway,
        )

        self.assertEqual(
            str(data["amount"]),
            str(self.payment.amount),
        )

        self.assertEqual(
            data["status"],
            self.payment.status,
        )

        self.assertIn(
            "created_at",
            data,
        )

        self.assertIn(
            "paid_at",
            data,
        )


class PaymentDetailSerializerTestCase(TestCase):
    def setUp(self):
        self.user = create_user()

        self.order = create_order(
            self.user,
        )

        self.payment = create_payment(
            order=self.order,
            authority="AUTH-123",
            ref_id="REF-123",
            amount=350000,
            status=PaymentStatus.SUCCESS,
            failure_reason="",
        )

    def test_serializer_fields(self):
        """
        باید تمام جزئیات پرداخت را برگرداند.
        """

        serializer = PaymentDetailSerializer(
            instance=self.payment,
        )

        data = serializer.data

        self.assertEqual(
            data["id"],
            self.payment.id,
        )

        self.assertEqual(
            data["order_number"],
            self.order.order_number,
        )

        self.assertEqual(
            data["gateway"],
            self.payment.gateway,
        )

        self.assertEqual(
            data["authority"],
            self.payment.authority,
        )

        self.assertEqual(
            data["ref_id"],
            self.payment.ref_id,
        )

        self.assertEqual(
            str(data["amount"]),
            str(self.payment.amount),
        )

        self.assertEqual(
            data["status"],
            self.payment.status,
        )

        self.assertEqual(
            data["failure_reason"],
            self.payment.failure_reason,
        )

        self.assertIn(
            "created_at",
            data,
        )

        self.assertIn(
            "updated_at",
            data,
        )

        self.assertIn(
            "paid_at",
            data,
        )