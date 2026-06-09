from decimal import Decimal

from django.test import TestCase

from users.models import User

from carts.models import Cart, CartItem

from carts.services.cart import (
    add_to_cart,
    clear_cart,
    remove_cart_item,
    update_cart_item,
)

from carts.services.coupon import remove_coupon

from carts.services.totals import calculate_cart_totals

from discounts.models import Coupon

from products.models import (
    Brand,
    Category,
    Product,
    ProductVariant,
)


class CartServicesTestCase(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            phone_number="09120000000",
            first_name="Test",
            last_name="User",
            password="123456",
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
            sku="S25-BLK-256",
        )

        self.cart = Cart.objects.create(
            user=self.user,
        )

    def test_add_to_cart(self):

        add_to_cart(
            cart=self.cart,
            variant=self.variant,
            quantity=2,
        )

        item = CartItem.objects.get(
            cart=self.cart,
            variant=self.variant,
        )

        self.assertEqual(item.quantity, 2)


    def test_add_to_cart_increase_quantity(self):
        CartItem.objects.create(
            cart=self.cart,
            variant=self.variant,
            quantity=1,
        )

        add_to_cart(
            cart=self.cart,
            variant=self.variant,
            quantity=2,
        )

        item = CartItem.objects.get(
            cart=self.cart,
            variant=self.variant,
        )

        self.assertEqual(item.quantity, 3)


    def test_update_cart_item(self):

        item = CartItem.objects.create(
            cart=self.cart,
            variant=self.variant,
            quantity=1,
        )

        update_cart_item(
            item=item,
            quantity=5,
        )

        item.refresh_from_db()

        self.assertEqual(item.quantity, 5)


    def test_remove_cart_item(self):

        item = CartItem.objects.create(
            cart=self.cart,
            variant=self.variant,
            quantity=1,
        )

        remove_cart_item(item)

        self.assertFalse(
            CartItem.objects.filter(
                pk=item.pk,
            ).exists()
        )


    def test_clear_cart(self):

        CartItem.objects.create(
            cart=self.cart,
            variant=self.variant,
            quantity=1,
        )

        CartItem.objects.create(
            cart=self.cart,
            variant=ProductVariant.objects.create(
                product=self.product,
                price=Decimal("5000000"),
                final_price=Decimal("5000000"),
                stock=5,
                sku="TEST-2",
            ),
            quantity=2,
        )

        clear_cart(cart=self.cart)

        self.assertEqual(
            self.cart.items.count(),
            0,
        )


    def test_remove_coupon(self):

        coupon = Coupon.objects.create(
            code="TEST10",
        )

        self.cart.coupon = coupon

        self.cart.save()

        remove_coupon(cart=self.cart)

        self.cart.refresh_from_db()

        self.assertIsNone(
            self.cart.coupon,
        )


    def test_calculate_cart_totals(self):

        CartItem.objects.create(
            cart=self.cart,
            variant=self.variant,
            quantity=2,
        )

        totals = calculate_cart_totals(
            self.cart,
        )

        self.assertEqual(
            totals["items_count"],
            2,
        )

        self.assertEqual(
            totals["subtotal"],
            Decimal("20000000"),
        )

        self.assertEqual(
            totals["total"],
            Decimal("18000000"),
        )


