from decimal import Decimal

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User

from carts.models import Cart, CartItem

from discounts.models import Coupon

from products.models import (
    Brand,
    Category,
    Product,
    ProductVariant,
)


class CartViewsTestCase(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            phone_number="09120000000",
            first_name="Test",
            last_name="User",
            password="123456",
        )

        self.client.force_authenticate(
            user=self.user,
        )

        self.category = Category.objects.create(
            name="موبایل",
            slug="mobile",
        )

        self.brand = Brand.objects.create(
            name="سامسونگ",
            slug="samsung",
        )

        self.product = Product.objects.create(
            name="Galaxy S25",
            slug="galaxy-s25",
            category=self.category,
            brand=self.brand,
        )

        self.variant = ProductVariant.objects.create(
            product=self.product,
            price=Decimal("10000000"),
            final_price=Decimal("9000000"),
            stock=10,
            sku="S25-256",
        )

        self.cart = Cart.objects.create(
            user=self.user,
        )


    def test_get_cart(self):

        url = reverse("cart-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn("cart", response.data)

        self.assertIn("totals", response.data)


    def test_add_item_to_cart(self):

        url = reverse("cart-item-list")

        response = self.client.post(
            url,
            {
                "variant": self.variant.id,
                "quantity": 2,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            self.cart.items.count(),
            1,
        )


    def test_add_item_with_invalid_quantity(self):

        url = reverse("cart-item-list")

        response = self.client.post(
            url,
            {
                "variant": self.variant.id,
                "quantity": 100,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


    def test_update_cart_item_quantity(self):

        item = CartItem.objects.create(
            cart=self.cart,
            variant=self.variant,
            quantity=1,
        )

        url = reverse(
            "cart-item-detail",
            kwargs={"pk": item.pk},
        )

        response = self.client.patch(
            url,
            {
                "quantity": 5,
            },
        )

        item.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            item.quantity,
            5,
        )


    def test_delete_cart_item(self):

        item = CartItem.objects.create(
            cart=self.cart,
            variant=self.variant,
            quantity=1,
        )

        url = reverse(
            "cart-item-detail",
            kwargs={"pk": item.pk},
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertFalse(
            CartItem.objects.filter(
                pk=item.pk,
            ).exists()
        )


    def test_user_cannot_modify_other_user_cart_item(self):

        other_user = User.objects.create_user(
            phone_number="09121111111",
            first_name="Other",
            last_name="User",
            password="123456",
        )

        other_cart = Cart.objects.create(
            user=other_user,
        )

        item = CartItem.objects.create(
            cart=other_cart,
            variant=self.variant,
            quantity=1,
        )

        url = reverse(
            "cart-item-detail",
            kwargs={"pk": item.pk},
        )

        response = self.client.patch(
            url,
            {
                "quantity": 5,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )


    def test_apply_coupon(self):

        coupon = Coupon.objects.create(
            code="TEST10",
        )

        url = reverse(
            "cart-apply-coupon",
        )

        response = self.client.post(
            url,
            {
                "code": coupon.code,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.cart.refresh_from_db()

        self.assertEqual(
            self.cart.coupon,
            coupon,
        )


    def test_apply_invalid_coupon(self):

        url = reverse(
            "cart-apply-coupon",
        )

        response = self.client.post(
            url,
            {
                "code": "INVALID",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


    def test_remove_coupon(self):

        coupon = Coupon.objects.create(
            code="TEST10",
        )

        self.cart.coupon = coupon

        self.cart.save()

        url = reverse(
            "cart-remove-coupon",
        )

        response = self.client.delete(url)

        self.cart.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIsNone(
            self.cart.coupon,
        )


    def test_anonymous_user_cannot_access_cart(self):

        self.client.force_authenticate(
            user=None,
        )

        url = reverse("cart-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )