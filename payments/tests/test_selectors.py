from django.test import TestCase

from orders.tests.factories import create_order, create_user

from payments.selectors import (
    get_order_payments,
    get_payment_by_authority,
    get_payment_by_id,
    get_payment_queryset,
    get_user_payments,
)
from shipping.tests.factories import create_shipping_method

from .factories import create_payment


class PaymentSelectorsTestCase(TestCase):
    def setUp(self):
        self.user = create_user(
            phone_number="+989121111111",
        )
        self.shipping_method = create_shipping_method()
        self.other_user = create_user(
            phone_number="+989121111112",
        )

    def test_get_payment_queryset(self):
        """
        باید QuerySet پرداخت‌ها را برگرداند.
        """

        payment = create_payment(
            order=create_order(
                user=self.user,
                shipping_method=self.shipping_method,
                order_number="ORD-000001",
            ),
        )

        queryset = get_payment_queryset()

        self.assertIn(
            payment,
            queryset,
        )

    def test_get_payment_by_id(self):
        """
        باید پرداخت را بر اساس شناسه برگرداند.
        """

        payment = create_payment(
            order=create_order(
                user=self.user,
                shipping_method=self.shipping_method,
                order_number="ORD-000001",
            ),
        )

        result = get_payment_by_id(
            payment.pk,
        )

        self.assertEqual(
            result,
            payment,
        )

    def test_get_payment_by_id_returns_none(self):
        """
        در صورت عدم وجود پرداخت باید None برگرداند.
        """

        result = get_payment_by_id(
            99999,
        )

        self.assertIsNone(
            result,
        )

    def test_get_payment_by_authority(self):
        """
        باید پرداخت را بر اساس Authority برگرداند.
        """

        payment = create_payment(
            order=create_order(
                user=self.user,
                shipping_method=self.shipping_method,
                order_number="ORD-000001",
            ),
            authority="AUTH-123456",
        )

        result = get_payment_by_authority(
            "AUTH-123456",
        )

        self.assertEqual(
            result,
            payment,
        )

    def test_get_payment_by_authority_returns_none(self):
        """
        در صورت عدم وجود Authority باید None برگرداند.
        """

        result = get_payment_by_authority(
            "INVALID-AUTHORITY",
        )

        self.assertIsNone(
            result,
        )

    def test_get_order_payments(self):
        """
        باید تمام پرداخت‌های سفارش را برگرداند.
        """

        order = create_order(
            user=self.user,
            shipping_method=self.shipping_method,
            order_number="ORD-000001",
        )

        payment_1 = create_payment(
            order=order,
            authority="AUTH-1",
        )

        payment_2 = create_payment(
            order=order,
            authority="AUTH-2",
        )

        other_order_payment = create_payment(
            order=create_order(
                user=self.user,
                shipping_method=self.shipping_method,
                order_number="ORD-000002",
            ),
            authority="AUTH-3",
        )

        queryset = get_order_payments(
            order,
        )

        self.assertEqual(
            queryset.count(),
            2,
        )

        self.assertIn(
            payment_1,
            queryset,
        )

        self.assertIn(
            payment_2,
            queryset,
        )

        self.assertNotIn(
            other_order_payment,
            queryset,
        )

    def test_get_user_payments(self):
        """
        باید فقط پرداخت‌های کاربر را برگرداند.
        """

        user_payment_1 = create_payment(
            order=create_order(
                user=self.user,
                shipping_method=self.shipping_method,
                order_number="ORD-000001",
            ),
            authority="AUTH-1",
        )

        user_payment_2 = create_payment(
            order=create_order(
                user=self.user,
                shipping_method=self.shipping_method,
                order_number="ORD-000002",
            ),
            authority="AUTH-2",
        )

        other_user_payment = create_payment(
            order=create_order(
                user=self.other_user,
                shipping_method=self.shipping_method,
                order_number="ORD-000003",
            ),
            authority="AUTH-3",
        )

        queryset = get_user_payments(
            self.user,
        )

        self.assertEqual(
            queryset.count(),
            2,
        )

        self.assertIn(
            user_payment_1,
            queryset,
        )

        self.assertIn(
            user_payment_2,
            queryset,
        )

        self.assertNotIn(
            other_user_payment,
            queryset,
        )