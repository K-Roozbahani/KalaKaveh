from decimal import Decimal
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model

from discounts.models import (
    CouponUsage,
    Discount,
)

from discounts.services.coupon import (
    validate_coupon,
    calculate_coupon_discount,
    register_coupon_usage,
)

from discounts.tests.factories import (
    create_coupon,
    create_discount,
)

from orders.tests.factories import (
    create_order,
)
from shipping.tests.factories import create_shipping_method

User = get_user_model()


class ValidateCouponTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            phone_number="+989121111111",
            password="123456",
        )

    def test_validate_coupon_success(self):

        coupon = create_coupon()

        result = validate_coupon(
            coupon=coupon,
            user=self.user,
        )

        self.assertEqual(
            result,
            coupon,
        )


class CalculateCouponDiscountTests(TestCase):

    def test_percent_discount(self):

        coupon = create_coupon(
            discount=create_discount(
                discount_type=Discount.PERCENT,
                value=20,
            )
        )

        result = calculate_coupon_discount(
            coupon=coupon,
            amount=100000,
        )

        self.assertEqual(
            result,
            Decimal("20000"),
        )

    def test_fixed_discount(self):

        coupon = create_coupon(
            discount=create_discount(
                discount_type=Discount.FIXED,
                value=30000,
            )
        )

        result = calculate_coupon_discount(
            coupon=coupon,
            amount=100000,
        )

        self.assertEqual(
            result,
            Decimal("30000"),
        )

    def test_fixed_discount_greater_than_amount(self):

        coupon = create_coupon(
            discount=create_discount(
                discount_type=Discount.FIXED,
                value=200000,
            )
        )

        result = calculate_coupon_discount(
            coupon=coupon,
            amount=100000,
        )

        self.assertEqual(
            result,
            Decimal("100000"),
        )

    def test_zero_amount(self):

        coupon = create_coupon()

        result = calculate_coupon_discount(
            coupon=coupon,
            amount=0,
        )

        self.assertEqual(
            result,
            Decimal("0"),
        )


class RegisterCouponUsageTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            phone_number="+989121111112",
            password="123456",
        )
        shipping_method = create_shipping_method()
        self.coupon = create_coupon()

        self.order = create_order(
            user=self.user,
            shipping_method=shipping_method,
        )

    def test_register_coupon_usage(self):

        register_coupon_usage(
            coupon=self.coupon,
            user=self.user,
            order=self.order,
        )

        self.assertTrue(
            CouponUsage.objects.filter(
                coupon=self.coupon,
                user=self.user,
            ).exists()
        )

        self.coupon.refresh_from_db()

        self.assertEqual(
            self.coupon.used_count,
            1,
        )