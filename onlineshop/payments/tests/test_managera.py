from django.test import TestCase

from orders.tests.factories import create_order,create_user

from payments.constants import PaymentStatus
from payments.models import Payment
from shipping.tests.factories import create_shipping_method

from .factories import create_payment


class PaymentManagerTestCase(TestCase):

    def setUp(self):
        self.user = create_user()
        self.shipping_method = create_shipping_method()

        self.order = create_order(
            shipping_method=self.shipping_method,
            user=self.user,
        )

    def test_pending_manager(self):
        pending_payment = create_payment(
            order=self.order,
            status=PaymentStatus.PENDING,
        )

        create_payment(
            order=self.order,
            status=PaymentStatus.FAILED,
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
        success_payment = create_payment(
            order=create_order(
                user=self.user,
                shipping_method=self.shipping_method,
            ),
            status=PaymentStatus.SUCCESS,
        )

        create_payment(
            order=self.order,
            status=PaymentStatus.FAILED,
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
        failed_payment = create_payment(
            order=self.order,
            status=PaymentStatus.FAILED,
        )

        create_payment(
            order=create_order(
                user=self.user,
                shipping_method=self.shipping_method,
            ),
            status=PaymentStatus.PENDING,
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
        canceled_payment = create_payment(
            order=create_order(
                user=self.user,
                shipping_method=self.shipping_method,
            ),
            status=PaymentStatus.CANCELED,
        )

        create_payment(
            order=create_order(
                user=self.user,
                shipping_method=self.shipping_method,
            ),
            status=PaymentStatus.PENDING,
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
        refunded_payment = create_payment(
            order=create_order(
                user=self.user,
                shipping_method=self.shipping_method,
            ),
            status=PaymentStatus.REFUNDED,
        )

        create_payment(
            order=create_order(
                user=self.user,
                shipping_method=self.shipping_method,
            ),
            status=PaymentStatus.PENDING,
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