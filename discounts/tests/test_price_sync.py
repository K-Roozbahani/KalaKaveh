from django.test import TestCase

from products.tests.factories import (
    create_product,
    create_variant,
)

from discounts.models import Discount, DiscountScope
from discounts.services.price_sync import (
    sync_variant_discount,
)


class PriceSyncServiceTest(TestCase):

    def setUp(self):

        self.product = create_product()

        self.variant = create_variant(
            product=self.product,
            price=100000,
            stock=10,
        )

    # --------------------------------------------------
    # 1. بدون هیچ تخفیف
    # --------------------------------------------------
    def test_no_discount(self):

        sync_variant_discount(
            variant=self.variant,
        )

        self.variant.refresh_from_db()

        self.assertEqual(
            self.variant.discount_amount,
            0,
        )

        self.assertEqual(
            self.variant.final_price,
            self.variant.price,
        )

    # --------------------------------------------------
    # 2. تخفیف درصدی
    # --------------------------------------------------
    def test_percent_discount(self):

        discount = Discount.objects.create(
            name="10% OFF",
            discount_type=Discount.PERCENT,
            value=10,
            priority=1,
            is_active=True,
            start_date="2025-01-01T00:00:00Z",
            end_date="2026-12-31T00:00:00Z",
        )

        DiscountScope.objects.create(
            discount=discount,
            variant=self.variant,
            target_type=4,
        )

        sync_variant_discount(
            variant=self.variant,
        )

        self.variant.refresh_from_db()

        self.assertEqual(
            self.variant.discount_amount,
            10000,
        )

        self.assertEqual(
            self.variant.final_price,
            90000,
        )

    # --------------------------------------------------
    # 3. تخفیف مبلغ ثابت
    # --------------------------------------------------
    def test_fixed_discount(self):

        discount = Discount.objects.create(
            name="Fixed OFF",
            discount_type=Discount.FIXED,
            value=20000,
            priority=1,
            is_active=True,
            start_date="2025-01-01T00:00:00Z",
            end_date="2026-12-31T00:00:00Z",
        )

        DiscountScope.objects.create(
            discount=discount,
            variant=self.variant,
            target_type=4,
        )

        sync_variant_discount(
            variant=self.variant,
        )

        self.variant.refresh_from_db()

        self.assertEqual(
            self.variant.discount_amount,
            20000,
        )

        self.assertEqual(
            self.variant.final_price,
            80000,
        )

    # --------------------------------------------------
    # 4. جلوگیری از منفی شدن قیمت
    # --------------------------------------------------
    def test_discount_cannot_exceed_price(self):

        discount = Discount.objects.create(
            name="Huge Discount",
            discount_type=Discount.FIXED,
            value=500000,
            priority=1,
            is_active=True,
            start_date="2025-01-01T00:00:00Z",
            end_date="2026-12-31T00:00:00Z",
        )

        DiscountScope.objects.create(
            discount=discount,
            variant=self.variant,
            target_type=4,
        )

        print("\nvariant_id: ", self.variant.id)
        print("create DiscountScope: ", DiscountScope.objects.values("variant_id"))

        print("VARIANT ID:", self.variant.id)

        print(
            "SCOPE EXISTS:",
            DiscountScope.objects.filter(variant_id=self.variant.id).exists()
        )

        sync_variant_discount(
            variant=self.variant,
        )

        self.variant.refresh_from_db()

        self.assertEqual(
            self.variant.discount_amount,
            100000,
        )

        self.assertEqual(
            self.variant.final_price,
            0,
        )

    # --------------------------------------------------
    # 5. تخفیف غیرفعال نباید اعمال شود
    # --------------------------------------------------
    def test_inactive_discount(self):

        discount = Discount.objects.create(
            name="Inactive",
            discount_type=Discount.PERCENT,
            value=50,
            priority=1,
            is_active=False,
            start_date="2025-01-01T00:00:00Z",
            end_date="2026-12-31T00:00:00Z",
        )

        DiscountScope.objects.create(
            discount=discount,
            variant=self.variant,
            target_type=4,
        )

        sync_variant_discount(
            variant=self.variant,
        )

        self.variant.refresh_from_db()

        self.assertEqual(
            self.variant.discount_amount,
            0,
        )

        self.assertEqual(
            self.variant.final_price,
            self.variant.price,
        )