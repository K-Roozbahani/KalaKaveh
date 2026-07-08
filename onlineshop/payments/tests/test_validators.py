from django.test import TestCase
from rest_framework.exceptions import ValidationError

from orders.tests.factories import create_order, create_user

from payments.constants import PaymentStatus
from payments.services.validators import (
    validate_payment_exists,
    validate_order_not_paid,
    validate_payment_amount,
)
from shipping.tests.factories import create_shipping_method

from .factories import create_payment


class PaymentValidatorsTestCase(TestCase):
    def setUp(self):
        self.user = create_user()
        self.shipping_method = create_shipping_method()
        self.order = create_order(
            self.user,
            shipping_method=self.shipping_method,
        )

    def test_validate_payment_exists_success(self):
        """
        اگر پرداخت وجود داشته باشد نباید خطا بدهد.
        """

        payment = create_payment(
            order=self.order,
        )

        # نباید Exception بدهد
        validate_payment_exists(payment)

    def test_validate_payment_exists_failed(self):
        """
        اگر پرداخت None باشد باید خطا بدهد.
        """

        with self.assertRaises(ValidationError):
            validate_payment_exists(None)

    def test_validate_order_not_paid_success(self):
        """
        اگر سفارش قبلاً پرداخت نشده باشد مشکلی ندارد.
        """

        validate_order_not_paid(self.order)

    def test_validate_order_not_paid_failed(self):
        """
        اگر سفارش قبلاً پرداخت شده باشد باید خطا بدهد.
        """

        self.order.paid_at = "2024-01-01T00:00:00Z"
        self.order.save()

        with self.assertRaises(ValidationError):
            validate_order_not_paid(self.order)

    # def test_validate_payment_is_pending_success(self):
    #     """
    #     اگر پرداخت در وضعیت Pending باشد معتبر است.
    #     """
    #
    #     payment = create_payment(
    #         order=self.order,
    #         status=PaymentStatus.PENDING,
    #     )
    #
    #     validate_payment_is_pending(payment)
    #
    # def test_validate_payment_is_pending_failed(self):
    #     """
    #     اگر پرداخت Pending نباشد باید خطا بدهد.
    #     """
    #
    #     payment = create_payment(
    #         order=self.order,
    #         status=PaymentStatus.SUCCESS,
    #     )
    #
    #     with self.assertRaises(ValidationError):
    #         validate_payment_is_pending(payment)

    def test_validate_payment_amount_success(self):
        """
        اگر مبلغ‌ها برابر باشند معتبر است.
        """

        validate_payment_amount(
            payment_amount=100000,
            gateway_amount=100000,
        )

    def test_validate_payment_amount_failed(self):
        """
        اگر مبلغ‌ها برابر نباشند باید خطا بدهد.
        """

        with self.assertRaises(ValidationError):
            validate_payment_amount(
                payment_amount=100000,
                gateway_amount=90000,
            )