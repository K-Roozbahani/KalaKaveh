from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model

from discounts.models import (
    Discount,
    Coupon,
    CouponUsage,
)

from orders.tests.factories import create_order

from shipping.tests.factories import create_shipping_method

from discounts.services.coupon import (
    validate_coupon,
    calculate_coupon_discount,
    register_coupon_usage,
)

User = get_user_model()


class CouponServiceTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.user = User.objects.create_user(
            phone_number="+989121111111",
            password="123456",
        )

        cls.discount_percent = Discount.objects.create(
            name="10% OFF",
            discount_type=Discount.PERCENT,
            value=10,
            priority=1,
            is_active=True,
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1),
        )

        cls.discount_fixed = Discount.objects.create(
            name="100000 OFF",
            discount_type=Discount.FIXED,
            value=100000,
            priority=1,
            is_active=True,
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1),
        )

        cls.coupon = Coupon.objects.create(
            code="TEST10",
            discount=cls.discount_percent,
            usage_limit=2,
            used_count=0,
            is_active=True,
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1),
        )

    def test_validate_coupon_success(self):

        result = validate_coupon(
            coupon=self.coupon,
            user=self.user,
        )

        self.assertEqual(
            result.pk,
            self.coupon.pk,
        )

    def test_calculate_percent_coupon(self):

        result = calculate_coupon_discount(
            coupon=self.coupon,
            amount=1000000,
        )

        self.assertEqual(
            result,
            Decimal("100000"),
        )

    def test_calculate_fixed_coupon(self):

        coupon = Coupon.objects.create(
            code="FIXED100",
            discount=self.discount_fixed,
            usage_limit=2,
            used_count=0,
            is_active=True,
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1),
        )

        result = calculate_coupon_discount(
            coupon=coupon,
            amount=1000000,
        )

        self.assertEqual(
            result,
            Decimal("100000"),
        )

    def test_fixed_coupon_cannot_exceed_amount(self):

        coupon = Coupon.objects.create(
            code="BIGFIX",
            discount=self.discount_fixed,
            usage_limit=2,
            used_count=0,
            is_active=True,
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1),
        )

        result = calculate_coupon_discount(
            coupon=coupon,
            amount=50000,
        )

        self.assertEqual(
            result,
            Decimal("50000"),
        )

    def test_coupon_usage_limit(self):

        self.coupon.used_count = 2
        self.coupon.save()

        with self.assertRaises(Exception):
            validate_coupon(
                coupon=self.coupon,
                user=self.user,
            )

    def test_prevent_duplicate_coupon_usage(self):
        shipping_method = create_shipping_method()

        order = create_order(
            user=self.user,
            shipping_method=shipping_method,
        )

        CouponUsage.objects.create(
            coupon=self.coupon,
            user=self.user,
            order=order,
        )

        with self.assertRaises(ValidationError):
            validate_coupon(
                coupon=self.coupon,
                user=self.user,
            )

    def test_register_coupon_usage(self):
        shipping_method = create_shipping_method()

        order = create_order(
            user=self.user,
            shipping_method=shipping_method,
        )

        register_coupon_usage(
            coupon=self.coupon,
            user=self.user,
            order=order,
        )

        self.coupon.refresh_from_db()

        self.assertEqual(
            self.coupon.used_count,
            1,
        )

        self.assertTrue(
            CouponUsage.objects.filter(
                coupon=self.coupon,
                user=self.user,
                order=order,
            ).exists()
        )

