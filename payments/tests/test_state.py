from django.test import TestCase

from payments.models import Payment
from payments.constants import (
    PaymentStatus,
    GatewayType,
)
from payments.services.state import (
    can_transition,
    transition_status,
    InvalidPaymentStateTransition,
)

from orders.tests.factories import (
    create_user,
    create_order,
)


class PaymentStateTestCase(TestCase):

    def setUp(self):

        self.user = create_user()

        self.order = create_order(
            user=self.user,
        )

        self.payment = Payment.objects.create(
            order=self.order,
            gateway=GatewayType.ZARINPAL,
            amount=100000,
        )



    def test_can_transition_pending_to_success(self):

        self.assertTrue(
            can_transition(
                PaymentStatus.PENDING,
                PaymentStatus.SUCCESS,
            )
        )


    def test_can_transition_pending_to_failed(self):

        self.assertTrue(
            can_transition(
                PaymentStatus.PENDING,
                PaymentStatus.FAILED,
            )
        )


    def test_can_transition_failed_to_pending(self):

        self.assertTrue(
            can_transition(
                PaymentStatus.FAILED,
                PaymentStatus.PENDING,
            )
        )


    def test_cannot_transition_success_to_failed(self):

        self.assertFalse(
            can_transition(
                PaymentStatus.SUCCESS,
                PaymentStatus.FAILED,
            )
        )


    def test_cannot_transition_refunded_to_success(self):

        self.assertFalse(
            can_transition(
                PaymentStatus.REFUNDED,
                PaymentStatus.SUCCESS,
            )
        )


    def test_transition_pending_to_success(self):

        transition_status(
            self.payment,
            PaymentStatus.SUCCESS,
        )

        self.payment.refresh_from_db()

        self.assertEqual(
            self.payment.status,
            PaymentStatus.SUCCESS,
        )


    def test_transition_pending_to_failed(self):

        transition_status(
            self.payment,
            PaymentStatus.FAILED,
        )

        self.payment.refresh_from_db()

        self.assertEqual(
            self.payment.status,
            PaymentStatus.FAILED,
        )


    def test_transition_failed_to_pending(self):

        self.payment.status = (
            PaymentStatus.FAILED
        )

        self.payment.save()

        transition_status(
            self.payment,
            PaymentStatus.PENDING,
        )

        self.payment.refresh_from_db()

        self.assertEqual(
            self.payment.status,
            PaymentStatus.PENDING,
        )


    def test_invalid_transition_success_to_failed(self):

        self.payment.status = (
            PaymentStatus.SUCCESS
        )

        self.payment.save()

        with self.assertRaises(
            InvalidPaymentStateTransition
        ):
            transition_status(
                self.payment,
                PaymentStatus.FAILED,
            )


    def test_invalid_transition_refunded_to_success(self):

        self.payment.status = (
            PaymentStatus.REFUNDED
        )

        self.payment.save()

        with self.assertRaises(
            InvalidPaymentStateTransition
        ):
            transition_status(
                self.payment,
                PaymentStatus.SUCCESS,
            )


    def test_transition_to_same_status_is_safe(self):

        self.payment.status = (
            PaymentStatus.SUCCESS
        )

        self.payment.save()

        result = transition_status(
            self.payment,
            PaymentStatus.SUCCESS,
        )

        self.payment.refresh_from_db()

        self.assertEqual(
            result.pk,
            self.payment.pk,
        )

        self.assertEqual(
            self.payment.status,
            PaymentStatus.SUCCESS,
        )