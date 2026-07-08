from unittest.mock import patch

from django.test import TestCase

from orders.constants import OrderStatus
from orders.services.completion import complete_paid_order

from orders.tests.factories import create_order
from payments.tests.factories import create_payment
from discounts.tests.factories import create_coupon
from shipping.tests.factories import create_shipping_method


class OrderCompletionServiceTest(TestCase):
    """
    تست سرویس تکمیل سفارش
    """

    def setUp(self):
        self.shipping_method = create_shipping_method()

    @patch(
        "orders.services.completion.register_coupon_usage"
    )
    def test_complete_order_without_coupon(
        self,
        mock_register_coupon,
    ):
        order = create_order(
            shipping_method=self.shipping_method,
            status=OrderStatus.PENDING,
        )

        payment = create_payment(
            order=order,
        )

        complete_paid_order(
            order=order,
            payment=payment,
        )

        order.refresh_from_db()

        self.assertEqual(
            order.status,
            OrderStatus.CONFIRMED,
        )

        mock_register_coupon.assert_not_called()

    @patch(
        "orders.services.completion.register_coupon_usage"
    )
    def test_complete_order_with_coupon(
        self,
        mock_register_coupon,
    ):
        coupon = create_coupon()

        order = create_order(
            shipping_method=self.shipping_method,
            status=OrderStatus.PENDING,
            coupon=coupon,
        )

        payment = create_payment(
            order=order,
        )

        complete_paid_order(
            order=order,
            payment=payment,
        )

        order.refresh_from_db()

        self.assertEqual(
            order.status,
            OrderStatus.CONFIRMED,
        )

        mock_register_coupon.assert_called_once()

    @patch(
        "orders.services.completion.register_coupon_usage"
    )
    def test_complete_paid_order_returns_order(
        self,
        mock_register_coupon,
    ):
        order = create_order(
            shipping_method=self.shipping_method,
        )

        payment = create_payment(
            order=order,
        )

        result = complete_paid_order(
            order=order,
            payment=payment,
        )

        self.assertEqual(
            result,
            order,
        )

    @patch(
        "orders.services.completion.register_coupon_usage"
    )
    def test_transaction_rolls_back_on_error(
        self,
        mock_register_coupon,
    ):
        coupon = create_coupon()

        order = create_order(
            shipping_method=self.shipping_method,
            status=OrderStatus.PENDING,
            coupon=coupon,
        )

        payment = create_payment(
            order=order,
        )

        mock_register_coupon.side_effect = RuntimeError()

        with self.assertRaises(RuntimeError):
            complete_paid_order(
                order=order,
                payment=payment,
            )

        order.refresh_from_db()

        self.assertEqual(
            order.status,
            OrderStatus.PENDING,
        )

    @patch("orders.services.completion.register_coupon_usage")
    def test_not_register_coupon_usage_when_order_has_no_coupon(
        self,
        mock_register_coupon_usage,
    ):
        order = create_order(
            shipping_method=self.shipping_method,
            coupon=None,
        )

        payment = create_payment(
            order=order,
        )

        complete_paid_order(
            order=order,
            payment=payment,
        )

        mock_register_coupon_usage.assert_not_called()


    @patch("orders.services.completion.register_coupon_usage")
    def test_register_coupon_usage_when_order_has_coupon(
            self,
            mock_register_coupon_usage,
    ):
        coupon = create_coupon()

        order = create_order(
            shipping_method=self.shipping_method,
            coupon=coupon,
        )

        payment = create_payment(
            order=order,
        )

        complete_paid_order(
            order=order,
            payment=payment,
        )

        mock_register_coupon_usage.assert_called_once_with(
            coupon=coupon,
            user=order.user,
            order=order,
        )
