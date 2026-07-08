from django.test import TestCase

from products.tests.factories import (
    create_product,
    create_variant,
)
from products.validators import (
    validate_product_is_active,
    validate_variant_is_active,
    validate_variant_has_stock,
    validate_quantity,
)


class ProductValidatorsTest(TestCase):

    def test_validate_product_is_active_success(self):

        product = create_product(is_active=True)

        validate_product_is_active(product=product)


    def test_validate_product_is_active_failed(self):

        product = create_product(is_active=False)

        with self.assertRaises(Exception):
            validate_product_is_active(product=product)


class VariantValidatorsTest(TestCase):

    def test_validate_variant_is_active_success(self):

        variant = create_variant(is_active=True)

        validate_variant_is_active(variant=variant)


    def test_validate_variant_is_active_failed(self):

        variant = create_variant(is_active=False)

        with self.assertRaises(Exception):
            validate_variant_is_active(variant=variant)


class StockValidatorsTest(TestCase):

    def test_validate_variant_has_stock_success(self):

        variant = create_variant(stock=10)

        validate_variant_has_stock(
            variant=variant,
            quantity=5,
        )


    def test_validate_variant_has_stock_failed(self):

        variant = create_variant(stock=2)

        with self.assertRaises(Exception):
            validate_variant_has_stock(
                variant=variant,
                quantity=5,
            )


class QuantityValidatorsTest(TestCase):

    def test_validate_quantity_success(self):

       validate_quantity(quantity=1)


    def test_validate_quantity_failed_zero(self):

        with self.assertRaises(Exception):
            validate_quantity(quantity=0)

    def test_validate_quantity_failed_negative(self):

        with self.assertRaises(Exception):
            validate_quantity(quantity=-5)

