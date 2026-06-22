from django.core.exceptions import ValidationError
from django.test import TestCase

from products.models import (
    Category,
    Product,
    ProductVariant,
)

from products.services.stock import (
    decrease_stock,
    increase_stock,
    set_stock,
)


class StockServiceTest(TestCase):
    """
    تست‌های سرویس مدیریت موجودی
    """

    @classmethod
    def setUpTestData(cls):

        cls.category = Category.objects.create(
            name="موبایل",
        )

        cls.product = Product.objects.create(
            name="آیفون 15",
            category=cls.category,
            is_active=True,
        )

        cls.variant = ProductVariant.objects.create(
            product=cls.product,
            sku="IPHONE15-128",
            price=100000000,
            stock=10,
            is_active=True,
        )

    def test_decrease_stock_success(self):
        """
        کاهش موجودی موفق
        """

        decrease_stock(
            variant=self.variant,
            quantity=3,
        )

        self.variant.refresh_from_db()

        self.assertEqual(
            self.variant.stock,
            7,
        )

    def test_decrease_stock_not_enough_stock(self):
        """
        خطا هنگام کمبود موجودی
        """

        with self.assertRaises(ValidationError):
            decrease_stock(
                variant=self.variant,
                quantity=20,
            )

    def test_decrease_stock_with_zero_quantity(self):
        """
        تعداد صفر مجاز نیست
        """

        with self.assertRaises(ValidationError):
            decrease_stock(
                variant=self.variant,
                quantity=0,
            )

    def test_decrease_stock_with_negative_quantity(self):
        """
        تعداد منفی مجاز نیست
        """

        with self.assertRaises(ValidationError):
            decrease_stock(
                variant=self.variant,
                quantity=-1,
            )

    def test_decrease_stock_inactive_product(self):
        """
        محصول غیرفعال قابل خرید نیست
        """

        self.product.is_active = False
        self.product.save()

        with self.assertRaises(ValidationError):
            decrease_stock(
                variant=self.variant,
                quantity=1,
            )

    def test_decrease_stock_inactive_variant(self):
        """
        تنوع غیرفعال قابل خرید نیست
        """

        self.variant.is_active = False
        self.variant.save()

        with self.assertRaises(ValidationError):
            decrease_stock(
                variant=self.variant,
                quantity=1,
            )

    def test_increase_stock_success(self):
        """
        افزایش موجودی
        """

        increase_stock(
            variant=self.variant,
            quantity=5,
        )

        self.variant.refresh_from_db()

        self.assertEqual(
            self.variant.stock,
            15,
        )

    def test_increase_stock_with_invalid_quantity(self):
        """
        تعداد نامعتبر برای افزایش موجودی
        """

        with self.assertRaises(ValidationError):
            increase_stock(
                variant=self.variant,
                quantity=0,
            )

    def test_set_stock_success(self):
        """
        تنظیم مستقیم موجودی
        """

        set_stock(
            variant=self.variant,
            quantity=50,
        )

        self.variant.refresh_from_db()

        self.assertEqual(
            self.variant.stock,
            50,
        )

    def test_set_stock_negative_quantity(self):
        """
        موجودی منفی مجاز نیست
        """

        with self.assertRaises(ValidationError):
            set_stock(
                variant=self.variant,
                quantity=-1,
            )