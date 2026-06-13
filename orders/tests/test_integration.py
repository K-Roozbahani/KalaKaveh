from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from users.models import User

from addresses.models import (
    Address,
    Province,
    City,
)

from carts.models import (
    Cart,
    CartItem,
)
from carts.constants import CartStatus

from orders.models import Order
from orders.services import create_order_from_cart

from products.models import (
    Product,
    ProductVariant,
)


class CartToOrderIntegrationTest(TestCase):
    """
    تست‌های یکپارچه (Integration)

    بررسی کامل فرآیند:

    Cart
        ↓
    Order
        ↓
    OrderItem
        ↓
    Stock Update
        ↓
    Cart Conversion
    """

    def setUp(self):
        """
        ایجاد داده‌های اولیه مورد نیاز تست‌ها
        """

        # کاربر
        self.user = User.objects.create_user(
            phone_number="09120000000",
            password="test123",
        )

        # استان
        self.province = Province.objects.create(
            name="تهران",
        )

        # شهر
        self.city = City.objects.create(
            province=self.province,
            name="تهران",
        )

        # آدرس
        self.address = Address.objects.create(
            user=self.user,
            title="خانه",

            receiver_name="علی رضایی",
            receiver_phone="09120000000",

            province=self.province,
            city=self.city,

            address_line="خیابان تست",

            postal_code="1234567890",
        )

        # محصول
        self.product = Product.objects.create(
            name="محصول تست",
            slug="test-product",
        )

        # واریانت محصول
        self.variant = ProductVariant.objects.create(
            product=self.product,

            sku="SKU-001",

            price=Decimal("100000"),

            stock=10,
        )

        # سبد خرید
        self.cart = Cart.objects.create(
            user=self.user,
            status=CartStatus.ACTIVE,
        )

        # آیتم سبد خرید
        CartItem.objects.create(
            cart=self.cart,
            variant=self.variant,
            quantity=2,
        )

    def test_create_order_successfully(self):
        """
        ثبت موفق سفارش از روی سبد خرید
        """

        order = create_order_from_cart(
            user=self.user,
            address_id=self.address.id,
            note="تحویل عصر",
        )

        self.assertIsNotNone(order)

        self.assertEqual(
            Order.objects.count(),
            1,
        )

        self.assertEqual(
            order.items.count(),
            1,
        )

    def test_order_item_created_correctly(self):
        """
        بررسی صحت اطلاعات OrderItem
        """

        order = create_order_from_cart(
            user=self.user,
            address_id=self.address.id,
        )

        item = order.items.first()

        self.assertEqual(
            item.quantity,
            2,
        )

        self.assertEqual(
            item.price,
            Decimal("100000"),
        )

    def test_address_snapshot_saved(self):
        """
        بررسی ذخیره Snapshot آدرس
        """

        order = create_order_from_cart(
            user=self.user,
            address_id=self.address.id,
        )

        self.assertEqual(
            order.address_snapshot["receiver_name"],
            "علی رضایی",
        )

        self.assertEqual(
            order.address_snapshot["postal_code"],
            "1234567890",
        )

    def test_product_snapshot_saved(self):
        """
        بررسی ذخیره Snapshot محصول
        """

        order = create_order_from_cart(
            user=self.user,
            address_id=self.address.id,
        )

        item = order.items.first()

        self.assertEqual(
            item.product_snapshot["product_name"],
            self.product.name,
        )

        self.assertEqual(
            item.product_snapshot["sku"],
            self.variant.sku,
        )

    def test_stock_reduced_after_order_creation(self):
        """
        بعد از ثبت سفارش باید موجودی کاهش پیدا کند
        """

        create_order_from_cart(
            user=self.user,
            address_id=self.address.id,
        )

        self.variant.refresh_from_db()

        self.assertEqual(
            self.variant.stock,
            8,
        )

    def test_cart_status_changed_to_converted(self):
        """
        بعد از ثبت سفارش باید وضعیت سبد خرید CONVERTED شود
        """

        create_order_from_cart(
            user=self.user,
            address_id=self.address.id,
        )

        self.cart.refresh_from_db()

        self.assertEqual(
            self.cart.status,
            CartStatus.CONVERTED,
        )

    def test_insufficient_stock_validation(self):
        """
        در صورت کمبود موجودی باید خطا ایجاد شود
        """

        self.variant.stock = 1
        self.variant.save()

        with self.assertRaises(ValidationError):
            create_order_from_cart(
                user=self.user,
                address_id=self.address.id,
            )

    def test_foreign_address_validation(self):
        """
        کاربر نباید بتواند از آدرس شخص دیگری استفاده کند
        """

        another_user = User.objects.create_user(
            phone_number="09121111111",
            password="test123",
        )

        foreign_address = Address.objects.create(
            user=another_user,
            title="خانه",

            receiver_name="کاربر دوم",
            receiver_phone="09121111111",

            province=self.province,
            city=self.city,

            address_line="آدرس دوم",

            postal_code="1111111111",
        )

        with self.assertRaises(ValidationError):
            create_order_from_cart(
                user=self.user,
                address_id=foreign_address.id,
            )

    def test_empty_cart_validation(self):
        """
        ثبت سفارش با سبد خرید خالی نباید ممکن باشد
        """

        CartItem.objects.all().delete()

        with self.assertRaises(ValidationError):
            create_order_from_cart(
                user=self.user,
                address_id=self.address.id,
            )

    def test_product_snapshot_should_not_change_after_product_update(self):
        """
        تغییر اطلاعات محصول نباید روی سفارش ثبت شده اثر بگذارد
        """

        order = create_order_from_cart(
            user=self.user,
            address_id=self.address.id,
        )

        self.product.name = "نام جدید محصول"
        self.product.save()

        item = order.items.first()

        self.assertEqual(
            item.product_snapshot["product_name"],
            "محصول تست",
        )

    def test_address_snapshot_should_not_change_after_address_update(self):
        """
        تغییر آدرس نباید روی Snapshot سفارش اثر بگذارد
        """

        order = create_order_from_cart(
            user=self.user,
            address_id=self.address.id,
        )

        self.address.receiver_name = "نام جدید"
        self.address.save()

        self.assertEqual(
            order.address_snapshot["receiver_name"],
            "علی رضایی",
        )