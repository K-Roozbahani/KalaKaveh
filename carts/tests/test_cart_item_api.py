from django.urls import reverse

from rest_framework import status

from carts.tests.base import CartAPITestCase

from orders.tests.factories import create_user


class CartItemAPIViewTests(CartAPITestCase):

    # =====================================================
    # Create
    # =====================================================

    def test_guest_can_add_item(self):
        """
        کاربر مهمان می‌تواند کالا به سبد خرید اضافه کند.
        """

        variant = self.create_variant(
            stock=10,
        )

        response = self.client.post(
            reverse("cart-item-list"),
            {
                "variant": variant.id,
                "quantity": 2,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["items_count"],
            2,
        )

        self.assertEqual(
            len(response.data["items"]),
            1,
        )

    def test_authenticated_user_can_add_item(self):
        """
        کاربر لاگین شده می‌تواند کالا اضافه کند.
        """

        user = self.login()

        variant = self.create_variant(
            stock=10,
        )

        response = self.client.post(
            reverse("cart-item-list"),
            {
                "variant": variant.id,
                "quantity": 3,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["items_count"],
            3,
        )

    # =====================================================
    # Update
    # =====================================================

    def test_guest_can_update_item(self):
        """
        کاربر مهمان می‌تواند تعداد کالا را تغییر دهد.
        """

        cart = self.get_cart()

        item = self.create_cart_item(
            cart=cart,
            variant=self.create_variant(stock=20),
            quantity=2,
        )

        response = self.client.patch(
            reverse(
                "cart-item-detail",
                args=[item.id],
            ),
            {
                "quantity": 5,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["items"][0]["quantity"],
            5,
        )

    def test_authenticated_user_can_update_item(self):
        """
        کاربر لاگین شده می‌تواند تعداد کالا را تغییر دهد.
        """

        user = self.login()

        cart = self.get_cart(
            user=user,
        )

        item = self.create_cart_item(
            cart=cart,
            variant=self.create_variant(stock=20),
            quantity=1,
        )

        response = self.client.patch(
            reverse(
                "cart-item-detail",
                args=[item.id],
            ),
            {
                "quantity": 4,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["items"][0]["quantity"],
            4,
        )

    # =====================================================
    # Delete
    # =====================================================

    def test_guest_can_remove_item(self):
        """
        کاربر مهمان می‌تواند آیتم را حذف کند.
        """

        cart = self.get_cart()

        item = self.create_cart_item(
            cart=cart,
            variant=self.create_variant(),
        )

        response = self.client.delete(
            reverse(
                "cart-item-detail",
                args=[item.id],
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["items_count"],
            0,
        )

    def test_authenticated_user_can_remove_item(self):
        """
        کاربر لاگین شده می‌تواند آیتم را حذف کند.
        """

        user = self.login()

        cart = self.get_cart(
            user=user,
        )

        item = self.create_cart_item(
            cart=cart,
            variant=self.create_variant(),
        )

        response = self.client.delete(
            reverse(
                "cart-item-detail",
                args=[item.id],
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["items_count"],
            0,
        )

    # =====================================================
    # Security
    # =====================================================

    def test_user_cannot_update_other_user_item(self):
        """
        کاربر نباید بتواند آیتم سبد خرید دیگران را تغییر دهد.
        """

        owner = create_user()

        cart = self.get_cart(
            user=owner,
        )

        item = self.create_cart_item(
            cart=cart,
            variant=self.create_variant(),
        )

        self.login()

        response = self.client.patch(
            reverse(
                "cart-item-detail",
                args=[item.id],
            ),
            {
                "quantity": 5,
            },
        )
        print("\nresponse.status_code:", response.status_code)
        print("\nresponse.data:", response.data, "\n")

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_user_cannot_remove_other_user_item(self):
        """
        کاربر نباید بتواند آیتم سبد خرید دیگران را حذف کند.
        """

        owner = create_user()

        cart = self.get_cart(
            user=owner,
        )

        item = self.create_cart_item(
            cart=cart,
            variant=self.create_variant(),
        )

        self.login()

        response = self.client.delete(
            reverse(
                "cart-item-detail",
                args=[item.id],
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_invalid_cart_item_returns_404(self):
        """
        شناسه نامعتبر باید 404 برگرداند.
        """

        response = self.client.patch(
            reverse(
                "cart-item-detail",
                args=[999999],
            ),
            {
                "quantity": 2,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )