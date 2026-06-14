from datetime import timedelta
from decimal import Decimal
from turtledemo.penrose import start

from django.test import TestCase
from django.utils import timezone
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError

from carts.services.merge import merge_guest_cart
from users.models import User

from carts.models import Cart, CartItem

from carts.services.cart import (
    add_to_cart,
    clear_cart,
    remove_cart_item,
    update_cart_item,
)

from carts.services.coupon import remove_coupon, validate_coupon

from carts.services.totals import calculate_cart_totals

from discounts.models import Coupon, Discount, DiscountTarget

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

        self.discount = Discount.objects.create(
            name="Unlimited Discount",
            discount_type=Discount.PERCENT,
            start_date=now(),
            end_date=now() + timedelta(days=7),
            value=10,
            is_active=True,
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
            discount_amount=Decimal("1000000"),
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
            discount=self.discount,
            start_date=now(),
            end_date=now() + timedelta(days=5)
        )

        self.cart.coupon = coupon

        self.cart.save()

        remove_coupon(cart=self.cart)

        self.cart.refresh_from_db()

        self.assertIsNone(
            self.cart.coupon,
        )


    def test_calculate_cart_totals(self):
        DiscountTarget.objects.create(
            discount=self.discount,
            target_type=4,
            variant=self.variant,
        )

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

    def test_merge_guest_cart(self):
        guest_cart = Cart.objects.create(
            session_key="guest-session",
        )

        CartItem.objects.create(
            cart=guest_cart,
            variant=self.variant,
            quantity=2,
        )

        merge_guest_cart(
            guest_cart=guest_cart,
            user_cart=self.cart,
        )

        self.assertEqual(
            self.cart.items.count(),
            1,
        )

        item = self.cart.items.first()

        self.assertEqual(
            item.quantity,
            2,
        )

        self.assertFalse(
            Cart.objects.filter(
                pk=guest_cart.pk,
            ).exists()
        )

    def test_merge_guest_cart_duplicate_variant(self):
        guest_cart = Cart.objects.create(
            session_key="guest-session",
        )

        CartItem.objects.create(
            cart=self.cart,
            variant=self.variant,
            quantity=2,
        )

        CartItem.objects.create(
            cart=guest_cart,
            variant=self.variant,
            quantity=3,
        )

        merge_guest_cart(
            guest_cart=guest_cart,
            user_cart=self.cart,
        )

        item = CartItem.objects.get(
            cart=self.cart,
            variant=self.variant,
        )

        self.assertEqual(
            item.quantity,
            5,
        )

    def test_merge_guest_cart_respects_stock_limit(self):
        self.variant.stock = 5

        self.variant.save(
            update_fields=["stock"],
        )

        guest_cart = Cart.objects.create(
            session_key="guest-session",
        )

        CartItem.objects.create(
            cart=self.cart,
            variant=self.variant,
            quantity=4,
        )

        CartItem.objects.create(
            cart=guest_cart,
            variant=self.variant,
            quantity=3,
        )

        merge_guest_cart(
            guest_cart=guest_cart,
            user_cart=self.cart,
        )

        item = CartItem.objects.get(
            cart=self.cart,
            variant=self.variant,
        )

        self.assertEqual(
            item.quantity,
            5,
        )

    def test_merge_guest_cart_removes_out_of_stock_items(self):
        self.variant.stock = 0

        self.variant.save(
            update_fields=["stock"],
        )

        guest_cart = Cart.objects.create(
            session_key="guest-session",
        )

        CartItem.objects.create(
            cart=guest_cart,
            variant=self.variant,
            quantity=2,
        )

        merge_guest_cart(
            guest_cart=guest_cart,
            user_cart=self.cart,
        )

        self.assertEqual(
            self.cart.items.count(),
            0,
        )

    def test_merge_guest_cart_multiple_items(self):
        second_variant = ProductVariant.objects.create(
            product=self.product,
            price=Decimal("5000000"),
            final_price=Decimal("4500000"),
            stock=10,
            sku="SECOND",
        )

        guest_cart = Cart.objects.create(
            session_key="guest-session",
        )

        CartItem.objects.create(
            cart=guest_cart,
            variant=self.variant,
            quantity=2,
        )

        CartItem.objects.create(
            cart=guest_cart,
            variant=second_variant,
            quantity=1,
        )

        merge_guest_cart(
            guest_cart=guest_cart,
            user_cart=self.cart,
        )

        self.assertEqual(
            self.cart.items.count(),
            2,
        )


    #کد تخفیف معتبر
    def test_validate_coupon_success(self):
        coupon = Coupon.objects.create(
            code="TEST10",
            discount=self.discount,
            start_date=now(),
            end_date=now() + timedelta(days=5)
        )

        result = validate_coupon(
            code="TEST10",
            cart=self.cart
        )

        self.assertEqual(
            result.pk,
            coupon.pk,
        )


    #کد تخفیف وجود ندارد
    def test_validate_coupon_not_found(self):
        with self.assertRaises(
                ValidationError,
        ):
            validate_coupon(
                code="INVALID",
                cart=self.cart,
            )



    #تخفیف غیرفعال است
    def test_validate_coupon_inactive_discount(self):
        discount = Discount.objects.create(
            name="Inactive Discount",
            discount_type=Discount.PERCENT,
            value=10,
            start_date=now(),
            end_date=now() + timedelta(days=7),
            is_active=False,
        )

        Coupon.objects.create(
            code="TEST10",
            discount=discount,
            start_date=now(),
            end_date=now() + timedelta(days=5)
        )

        with self.assertRaises(
                ValidationError,
        ):
            validate_coupon(
                code="TEST10",
                cart=self.cart
            )


    #زمان شروع هنوز نرسیده
    def test_validate_coupon_not_started(self):
        discount = Discount.objects.create(
            name="Future Discount",
            discount_type=Discount.PERCENT,
            value=10,
            is_active=True,
            start_date=timezone.now() + timedelta(days=1),
            end_date=now() + timedelta(days=7)
        )

        Coupon.objects.create(
            code="TEST10",
            discount=discount,
            start_date=now(),
            end_date=now() + timedelta(days=7),

        )

        with self.assertRaises(
                ValidationError,
        ):
            validate_coupon(
                code="TEST10",
                cart=self.cart,
            )


    #زمان تخفیف تمام شده
    def test_validate_coupon_expired(self):
        discount = Discount.objects.create(
            name="Expired Discount",
            discount_type=Discount.PERCENT,
            value=10,
            is_active=True,
            start_date=now() - timedelta(days=5),
            end_date=timezone.now() - timedelta(days=1),
        )

        Coupon.objects.create(
            code="TEST10",
            discount=discount,
            start_date=now(),
            end_date=timezone.now() + timedelta(days=7),
        )

        with self.assertRaises(
                ValidationError,
        ):
            validate_coupon(
                code="TEST10",
                cart=self.cart,
            )


    #ظرفیت استفاده تکمیل شده
    def test_validate_coupon_usage_limit_reached(self):

        Coupon.objects.create(
            code="TEST10",
            discount=self.discount,
            usage_limit=10,
            used_count=10,
            start_date=now(),
            end_date=now() + timedelta(days=8),
        )

        with self.assertRaises(
                ValidationError,
        ):
            validate_coupon(
                code="TEST10",
                cart=self.cart,
            )


    #یک استفاده تا سقف باقی مانده
    def test_validate_coupon_usage_limit_not_reached(self):

        coupon = Coupon.objects.create(
            code="TEST10",
            discount=self.discount,
            usage_limit=10,
            used_count=9,
            start_date=now(),
            end_date=now() + timedelta(days=7),
        )

        result = validate_coupon(
            code="TEST10",
            cart=self.cart,
        )

        self.assertEqual(
            result.pk,
            coupon.pk,
        )


    #بدون محدودیت استفاده
    #     کوپن بدون محدودیت استفاده را پشتیبانی نمی‌کنی
    # def test_validate_coupon_without_usage_limit(self):
    #
    #     coupon = Coupon.objects.create(
    #         code="TEST10",
    #         discount=self.discount,
    #         usage_limit=None,
    #     )
    #
    #     result = validate_coupon(
    #         code="TEST10",
    #     )
    #
    #     self.assertEqual(
    #         result.pk,
    #         coupon.pk,
    #     )


