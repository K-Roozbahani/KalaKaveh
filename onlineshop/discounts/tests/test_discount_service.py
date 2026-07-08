from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from discounts.models import (
    Discount,
    DiscountScope,
)

from discounts.services.discount import (
    calculate_discount_amount,
    calculate_variant_price,
    refresh_variant_price,
    refresh_variants_prices,
)

from products.models import (
    Category,
    Product,
    ProductVariant,
)


class DiscountServiceTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.category = Category.objects.create(
            name="موبایل",
        )

        cls.product = Product.objects.create(
            name="آیفون 15",
            category=cls.category,
            is_active=True,
        )

        cls.variant = ProductVariant.objects.create(
            product=cls.product,
            sku="IPHONE15-128",
            price=1000000,
            stock=10,
            is_active=True,
        )

    def create_discount(
        self,
        *,
        discount_type,
        value,
        priority=1,
    ):
        return Discount.objects.create(
            name="Test Discount",
            discount_type=discount_type,
            value=value,
            priority=priority,
            is_active=True,
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1),
        )

    def test_calculate_percent_discount_amount(self):

        discount = self.create_discount(
            discount_type=Discount.PERCENT,
            value=10,
        )

        result = calculate_discount_amount(
            price=1000000,
            discount=discount,
        )

        self.assertEqual(
            result,
            100000,
        )

    def test_calculate_fixed_discount_amount(self):

        discount = self.create_discount(
            discount_type=Discount.FIXED,
            value=150000,
        )

        result = calculate_discount_amount(
            price=1000000,
            discount=discount,
        )

        self.assertEqual(
            result,
            150000,
        )

    def test_fixed_discount_cannot_be_greater_than_price(self):

        discount = self.create_discount(
            discount_type=Discount.FIXED,
            value=2000000,
        )

        result = calculate_discount_amount(
            price=1000000,
            discount=discount,
        )

        self.assertEqual(
            result,
            1000000,
        )

    def test_calculate_variant_price_without_discount(self):

        result = calculate_variant_price(
            variant=self.variant,
        )

        self.assertEqual(
            result["discount_amount"],
            0,
        )

        self.assertEqual(
            result["final_price"],
            1000000,
        )

        self.assertIsNone(
            result["discount"],
        )

    def test_calculate_variant_price_with_discount(self):

        discount = self.create_discount(
            discount_type=Discount.PERCENT,
            value=20,
        )

        DiscountScope.objects.create(
            discount=discount,
            variant=self.variant,
            target_type=4,
        )

        result = calculate_variant_price(
            variant=self.variant,
        )

        self.assertEqual(
            result["discount_amount"],
            200000,
        )

        self.assertEqual(
            result["final_price"],
            800000,
        )

    def test_highest_priority_discount_wins(self):

        low_priority_discount = self.create_discount(
            discount_type=Discount.PERCENT,
            value=10,
            priority=10,
        )

        high_priority_discount = self.create_discount(
            discount_type=Discount.PERCENT,
            value=30,
            priority=100,
        )

        DiscountScope.objects.create(
            discount=low_priority_discount,
            variant=self.variant,
            target_type=4,
        )

        DiscountScope.objects.create(
            discount=high_priority_discount,
            variant=self.variant,
            target_type=4,
        )

        result = calculate_variant_price(
            variant=self.variant,
        )

        self.assertEqual(
            result["discount_amount"],
            300000,
        )

        self.assertEqual(
            result["final_price"],
            700000,
        )

        self.assertEqual(
            result["discount"].pk,
            high_priority_discount.pk,
        )

    def test_refresh_variant_price(self):

        discount = self.create_discount(
            discount_type=Discount.PERCENT,
            value=25,
        )

        DiscountScope.objects.create(
            discount=discount,
            variant=self.variant,
            target_type=4,
        )

        refresh_variant_price(
            variant=self.variant,
        )

        self.variant.refresh_from_db()

        self.assertEqual(
            self.variant.discount_amount,
            250000,
        )

        self.assertEqual(
            self.variant.final_price,
            750000,
        )

    def test_refresh_variants_prices(self):

        discount = self.create_discount(
            discount_type=Discount.PERCENT,
            value=10,
        )

        DiscountScope.objects.create(
            discount=discount,
            variant=self.variant,
            target_type=4,
        )

        count = refresh_variants_prices(
            queryset=ProductVariant.objects.all(),
        )

        self.variant.refresh_from_db()

        self.assertEqual(
            count,
            1,
        )

        self.assertEqual(
            self.variant.discount_amount,
            100000,
        )

        self.assertEqual(
            self.variant.final_price,
            900000,
        )