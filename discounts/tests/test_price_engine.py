from django.test import TestCase

from discounts.models import Discount
from discounts.services.price_engine import (
    PriceSnapshot,
    calculate_discount_amount,
    calculate_variant_price,
)

from discounts.tests.factories import (
    create_discount,
    create_discount_scope,
)

from products.tests.factories import (
    create_product,
    create_variant,
    create_category,
    create_brand,
)


class CalculateDiscountAmountTests(TestCase):

    def test_percent_discount(self):
        discount = create_discount(
            discount_type=Discount.PERCENT,
            value=20,
        )

        result = calculate_discount_amount(
            price=100000,
            discount=discount,
        )

        self.assertEqual(
            result,
            20000,
        )

    def test_fixed_discount(self):
        discount = create_discount(
            discount_type=Discount.FIXED,
            value=30000,
        )

        result = calculate_discount_amount(
            price=100000,
            discount=discount,
        )

        self.assertEqual(
            result,
            30000,
        )

    def test_fixed_discount_cannot_be_greater_than_price(self):
        discount = create_discount(
            discount_type=Discount.FIXED,
            value=200000,
        )

        result = calculate_discount_amount(
            price=100000,
            discount=discount,
        )

        self.assertEqual(
            result,
            100000,
        )


class CalculateVariantPriceTests(TestCase):

    def test_without_discount(self):
        variant = create_variant(
            price=100000,
        )

        snapshot = calculate_variant_price(
            variant=variant,
        )

        self.assertIsInstance(
            snapshot,
            PriceSnapshot,
        )

        self.assertEqual(
            snapshot.base_price,
            100000,
        )

        self.assertEqual(
            snapshot.discount_amount,
            0,
        )

        self.assertEqual(
            snapshot.final_price,
            100000,
        )

        self.assertIsNone(
            snapshot.discount,
        )

        self.assertIsNone(
            snapshot.scope,
        )

    def test_variant_discount(self):
        variant = create_variant(
            price=100000,
        )

        discount = create_discount(
            value=20,
        )

        create_discount_scope(
            discount=discount,
            variant=variant,
        )

        snapshot = calculate_variant_price(
            variant=variant,
        )

        self.assertEqual(
            snapshot.discount_amount,
            20000,
        )

        self.assertEqual(
            snapshot.final_price,
            80000,
        )

        self.assertEqual(
            snapshot.discount,
            discount,
        )

    def test_product_discount(self):
        product = create_product()

        variant = create_variant(
            product=product,
            price=100000,
        )

        discount = create_discount(
            value=10,
        )

        create_discount_scope(
            discount=discount,
            product=product,
        )

        snapshot = calculate_variant_price(
            variant=variant,
        )

        self.assertEqual(
            snapshot.final_price,
            90000,
        )

    def test_category_discount(self):
        category = create_category()

        product = create_product(
            category=category,
        )

        variant = create_variant(
            product=product,
            price=100000,
        )

        discount = create_discount(
            value=15,
        )

        create_discount_scope(
            discount=discount,
            category=category,
        )

        snapshot = calculate_variant_price(
            variant=variant,
        )

        self.assertEqual(
            snapshot.final_price,
            85000,
        )

    def test_brand_discount(self):
        brand = create_brand()

        product = create_product(
            brand=brand,
        )

        variant = create_variant(
            product=product,
            price=100000,
        )

        discount = create_discount(
            value=25,
        )

        create_discount_scope(
            discount=discount,
            brand=brand,
        )

        snapshot = calculate_variant_price(
            variant=variant,
        )

        self.assertEqual(
            snapshot.final_price,
            75000,
        )

    def test_higher_priority_discount_is_selected(self):
        variant = create_variant(
            price=100000,
        )

        low = create_discount(
            value=10,
            priority=10,
        )

        high = create_discount(
            value=30,
            priority=100,
        )

        create_discount_scope(
            discount=low,
            variant=variant,
        )

        create_discount_scope(
            discount=high,
            variant=variant,
        )

        snapshot = calculate_variant_price(
            variant=variant,
        )

        self.assertEqual(
            snapshot.discount,
            high,
        )

        self.assertEqual(
            snapshot.final_price,
            70000,
        )

    def test_final_price_never_becomes_negative(self):
        variant = create_variant(
            price=50000,
        )

        discount = create_discount(
            discount_type=Discount.FIXED,
            value=100000,
        )

        create_discount_scope(
            discount=discount,
            variant=variant,
        )

        snapshot = calculate_variant_price(
            variant=variant,
        )

        self.assertEqual(
            snapshot.discount_amount,
            50000,
        )

        self.assertEqual(
            snapshot.final_price,
            0,
        )