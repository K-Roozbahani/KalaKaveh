from django.urls import reverse

from rest_framework import status

from carts.tests.base import CartAPITestCase


class CartAPIViewTests(CartAPITestCase):

    def test_guest_can_get_empty_cart(self):
        """
        کاربر مهمان می‌تواند سبد خرید خالی دریافت کند.
        """

        response = self.client.get(
            reverse("cart-list"),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["items_count"],
            0,
        )

        self.assertEqual(
            len(response.data["items"]),
            0,
        )

    def test_authenticated_user_can_get_cart(self):
        """
        کاربر لاگین شده سبد خرید خود را دریافت می‌کند.
        """

        user = self.login()

        cart = self.get_cart(
            user=user,
        )

        variant = self.create_variant()

        self.create_cart_item(
            cart=cart,
            variant=variant,
            quantity=2,
        )

        response = self.client.get(
            reverse("cart-list"),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["items_count"],
            2,
        )

        self.assertEqual(
            len(response.data["items"]),
            1,
        )

    def test_guest_can_clear_cart(self):
        """
        کاربر مهمان می‌تواند سبد خرید خود را پاک کند.
        """

        cart = self.get_cart()

        variant = self.create_variant()

        self.create_cart_item(
            cart=cart,
            variant=variant,
            quantity=3,
        )

        response = self.client.delete(
            reverse("cart-clear"),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["items_count"],
            0,
        )

        self.assertEqual(
            len(response.data["items"]),
            0,
        )

    def test_authenticated_user_can_clear_cart(self):
        """
        کاربر لاگین شده می‌تواند سبد خرید خود را پاک کند.
        """

        user = self.login()

        cart = self.get_cart(
            user=user,
        )

        variant = self.create_variant()

        self.create_cart_item(
            cart=cart,
            variant=variant,
            quantity=5,
        )

        response = self.client.delete(
            reverse("cart-clear"),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["items_count"],
            0,
        )

        self.assertEqual(
            len(response.data["items"]),
            0,
        )

    def test_clear_empty_cart(self):
        """
        پاک کردن سبد خرید خالی باید موفق باشد.
        """

        response = self.client.delete(
            reverse("cart-clear"),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["items_count"],
            0,
        )

        self.assertEqual(
            len(response.data["items"]),
            0,
        )

    def test_guest_and_authenticated_cart_are_independent(self):
        """
        سبد خرید مهمان و کاربر لاگین شده باید مستقل باشند.
        """

        # -----------------------------
        # Guest Cart
        # -----------------------------
        guest_cart = self.get_cart()

        guest_variant = self.create_variant()

        self.create_cart_item(
            cart=guest_cart,
            variant=guest_variant,
            quantity=2,
        )

        response = self.client.get(
            reverse("cart-list"),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["items_count"],
            2,
        )

        self.assertEqual(
            len(response.data["items"]),
            1,
        )

        # -----------------------------
        # Login
        # -----------------------------
        user = self.login()

        response = self.client.get(
            reverse("cart-list"),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        # کاربر باید سبد خرید مستقل داشته باشد.
        self.assertEqual(
            response.data["items_count"],
            0,
        )

        self.assertEqual(
            len(response.data["items"]),
            0,
        )