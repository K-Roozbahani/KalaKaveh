from unittest.mock import patch

from django.test import TestCase

from carts.constants import CartStatus
from carts.services.cart import (
    add_to_cart,
    clear_cart,
    get_or_create_cart,
    remove_cart_item,
    update_cart_item,
)
from carts.tests.factories import (
    create_cart,
    create_cart_item,
)

from orders.tests.factories import create_user
from products.tests.factories import create_variant


class GetOrCreateCartTests(TestCase):
    """
    تست دریافت یا ایجاد سبد خرید
    """

    def test_get_or_create_cart_for_user(self):
        user = create_user()

        cart = get_or_create_cart(
            user=user,
        )

        self.assertEqual(
            cart.user,
            user,
        )

        self.assertEqual(
            cart.status,
            CartStatus.ACTIVE,
        )

    def test_return_existing_cart(self):
        user = create_user()

        cart = create_cart(
            user=user,
        )

        result = get_or_create_cart(
            user=user,
        )

        self.assertEqual(
            result.id,
            cart.id,
        )

    def test_get_or_create_guest_cart(self):
        cart = get_or_create_cart(
            session_key="guest-session",
        )

        self.assertEqual(
            cart.session_key,
            "guest-session",
        )

        self.assertEqual(
            cart.status,
            CartStatus.ACTIVE,
        )


class AddToCartTests(TestCase):
    """
    تست افزودن کالا به سبد
    """

    @patch("carts.services.cart.ensure_variant_can_be_purchased")
    def test_add_new_item(
        self,
        mock_stock,
    ):
        user = create_user()

        cart = create_cart(
            user=user,
        )

        variant = create_variant()

        item = add_to_cart(
            cart=cart,
            variant=variant,
            quantity=2,
        )

        self.assertEqual(
            item.quantity,
            2,
        )

        mock_stock.assert_called_once_with(
            variant=variant,
            quantity=2,
        )

    @patch("carts.services.cart.ensure_variant_can_be_purchased")
    def test_increase_existing_item(
        self,
        mock_stock,
    ):
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

        item = add_to_cart(
            cart=cart,
            variant=variant,
            quantity=3,
        )

        self.assertEqual(
            item.quantity,
            5,
        )

        mock_stock.assert_called_once_with(
            variant=variant,
            quantity=5,
        )


class UpdateCartItemTests(TestCase):
    """
    تست بروزرسانی تعداد
    """

    @patch("carts.services.cart.ensure_variant_can_be_purchased")
    def test_update_quantity(
        self,
        mock_stock,
    ):
        user = create_user()

        cart = create_cart(
            user=user,
        )

        variant = create_variant()

        item = create_cart_item(
            cart=cart,
            variant=variant,
            quantity=1,
        )

        update_cart_item(
            item=item,
            quantity=4,
        )

        item.refresh_from_db()

        self.assertEqual(
            item.quantity,
            4,
        )

        mock_stock.assert_called_once_with(
            variant=variant,
            quantity=4,
        )


class RemoveCartItemTests(TestCase):
    """
    تست حذف آیتم
    """

    def test_remove_cart_item(self):
        user = create_user()

        cart = create_cart(
            user=user,
        )

        variant = create_variant()

        item = create_cart_item(
            cart=cart,
            variant=variant,
        )

        remove_cart_item(
            item=item,
        )

        self.assertFalse(
            cart.items.exists(),
        )


class ClearCartTests(TestCase):
    """
    تست پاک کردن سبد خرید
    """

    def test_clear_cart(self):
        user = create_user()

        cart = create_cart(
            user=user,
        )

        create_cart_item(
            cart=cart,
            variant=create_variant(),
        )

        create_cart_item(
            cart=cart,
            variant=create_variant(),
        )

        clear_cart(
            cart=cart,
        )

        self.assertEqual(
            cart.items.count(),
            0,
        )