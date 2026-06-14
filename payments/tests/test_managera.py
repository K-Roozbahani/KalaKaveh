from django.test import TestCase

from apps.orders.models import Order
from apps.payments.constants import (
    GatewayType,
    PaymentStatus,
)
from apps.payments.models import Payment

from tests.factories import (
    user_factory,
    order_factory,
)


class PaymentManagerTestCase(TestCase):

    def setUp(self):
        self.user = user_factory()

        self.order = order_factory(
            user=self.user,
        )

    def create_payment(
        self,
        status,
    ):
        return Payment.objects.create(
            order=self.order,
            gateway=GatewayType.ZARINPAL,
            amount=100000,
            status=status,
        )

    def test_pending_manager(self):
        pending_payment = self.create_payment(
            PaymentStatus.PENDING,
        )

        self.create_payment(
            PaymentStatus.FAILED,
        )

        queryset = Payment.objects.pending()

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertIn(
            pending_payment,
            queryset,
        )

    def test_successful_manager(self):
        success_payment = self.create_payment(
            PaymentStatus.SUCCESS,
        )

        self.create_payment(
            PaymentStatus.FAILED,
        )

        queryset = Payment.objects.successful()

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertIn(
            success_payment,
            queryset,
        )

    def test_failed_manager(self):
        failed_payment = self.create_payment(
            PaymentStatus.FAILED,
        )

        self.create_payment(
            PaymentStatus.PENDING,
        )

        queryset = Payment.objects.failed()

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertIn(
            failed_payment,
            queryset,
        )

    def test_canceled_manager(self):
        canceled_payment = self.create_payment(
            PaymentStatus.CANCELED,
        )

        self.create_payment(
            PaymentStatus.PENDING,
        )

        queryset = Payment.objects.canceled()

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertIn(
            canceled_payment,
            queryset,
        )

    def test_refunded_manager(self):
        refunded_payment = self.create_payment(
            PaymentStatus.REFUNDED,
        )

        self.create_payment(
            PaymentStatus.PENDING,
        )

        queryset = Payment.objects.refunded()

        self.assertEqual(
            queryset.count(),
            1,
        )

        self.assertIn(
            refunded_payment,
            queryset,
        )