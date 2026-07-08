from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase

from carts.services.pricing import calculate_cart_totals

from carts.tests.factories import (
    create_cart,
    create_cart_item,
)

from products.tests.factories import (
    create_variant,
)

from orders.tests.factories import (
    create_user,
)


class CalculateCartTotalsTests(TestCase):
    """
    تست سرویس calculate_cart_totals
    """

    @patch("carts.services.pricing.calculate_variant_price")
    def test_calculate_cart_totals_without_coupon(
        self,
        mock_calculate_variant_price,
    ):
        """
        محاسبه صحیح خلاصه مالی بدون کوپن
        """

        user = create_user()

        cart = create_cart(
            user=user,
        )

        variant = create_variant()

        create_cart_item(
            cart=cart,
            variant=variant,
            quantity=2,
        )

        mock_calculate_variant_price.return_value.base_price = 100_000
        mock_calculate_variant_price.return_value.discount_amount = 20_000
        mock_calculate_variant_price.return_value.final_price = 80_000

        result = calculate_cart_totals(
            cart=cart,
        )

        self.assertEqual(
            result["items_count"],
            2,
        )

        self.assertEqual(
            result["subtotal"],
            Decimal("200000"),
        )

        self.assertEqual(
            result["product_discount"],
            Decimal("40000"),
        )

        self.assertEqual(
            result["coupon_discount"],
            Decimal("0"),
        )

        self.assertEqual(
            result["discount"],
            Decimal("40000"),
        )

        self.assertEqual(
            result["total"],
            Decimal("160000"),
        )

    @patch("carts.services.pricing.calculate_coupon_discount")
    @patch("carts.services.pricing.calculate_variant_price")
    def test_calculate_cart_totals_with_coupon(
        self,
        mock_calculate_variant_price,
        mock_calculate_coupon_discount,
    ):
        """
        محاسبه صحیح خلاصه مالی با کوپن
        """

        user = create_user()

        cart = create_cart(
            user=user,
        )

        variant = create_variant()

        coupon = object()

        create_cart_item(
            cart=cart,
            variant=variant,
            quantity=1,
        )

        mock_calculate_variant_price.return_value.base_price = 100_000
        mock_calculate_variant_price.return_value.discount_amount = 10_000
        mock_calculate_variant_price.return_value.final_price = 90_000

        mock_calculate_coupon_discount.return_value = Decimal("5000")

        result = calculate_cart_totals(
            cart=cart,
            coupon=coupon,
        )

        mock_calculate_coupon_discount.assert_called_once_with(
            coupon=coupon,
            amount=Decimal("90000"),
        )

        self.assertEqual(
            result["coupon_discount"],
            Decimal("5000"),
        )

        self.assertEqual(
            result["discount"],
            Decimal("15000"),
        )

        self.assertEqual(
            result["total"],
            Decimal("85000"),
        )

    def test_calculate_empty_cart(self):
        """
        محاسبه سبد خرید خالی
        """

        user = create_user()

        cart = create_cart(
            user=user,
        )

        result = calculate_cart_totals(
            cart=cart,
        )

        self.assertEqual(
            result,
            {
                "items_count": 0,
                "subtotal": Decimal("0"),
                "product_discount": Decimal("0"),
                "coupon_discount": Decimal("0"),
                "discount": Decimal("0"),
                "total": Decimal("0"),
            },
        )