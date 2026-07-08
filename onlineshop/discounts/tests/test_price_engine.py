from django.test import TestCase

from discounts.models import Discount
from discounts.services.price_sync import (
    sync_variant_discount,
)

from discounts.tests.factories import (
    create_discount,
    create_discount_scope,
)

from products.tests.factories import (
    create_variant,
)


class SyncVariantDiscountTests(TestCase):

    def test_sync_variant_without_discount(self):
        """
        در صورت نبود تخفیف، Snapshot باید برابر قیمت اصلی باشد.
        """

        variant = create_variant(
            price=100000,
            discount_amount=999,
            final_price=999,
        )

        sync_variant_discount(
            variant=variant,
        )

        variant.refresh_from_db()

        self.assertEqual(
            variant.discount_amount,
            0,
        )

        self.assertEqual(
            variant.final_price,
            100000,
        )

    def test_sync_variant_with_percent_discount(self):
        """
        Snapshot باید بر اساس تخفیف درصدی بروزرسانی شود.
        """

        variant = create_variant(
            price=100000,
        )

        discount = create_discount(
            discount_type=Discount.PERCENT,
            value=20,
        )

        create_discount_scope(
            discount=discount,
            variant=variant,
        )

        sync_variant_discount(
            variant=variant,
        )

        variant.refresh_from_db()

        self.assertEqual(
            variant.discount_amount,
            20000,
        )

        self.assertEqual(
            variant.final_price,
            80000,
        )

    def test_sync_variant_with_fixed_discount(self):
        """
        Snapshot باید بر اساس تخفیف مبلغ ثابت بروزرسانی شود.
        """

        variant = create_variant(
            price=100000,
        )

        discount = create_discount(
            discount_type=Discount.FIXED,
            value=30000,
        )

        create_discount_scope(
            discount=discount,
            variant=variant,
        )

        sync_variant_discount(
            variant=variant,
        )

        variant.refresh_from_db()

        self.assertEqual(
            variant.discount_amount,
            30000,
        )

        self.assertEqual(
            variant.final_price,
            70000,
        )

    def test_sync_variant_fixed_discount_cannot_make_price_negative(self):
        """
        قیمت نهایی نباید منفی شود.
        """

        variant = create_variant(
            price=50000,
        )

        discount = create_discount(
            discount_type=Discount.FIXED,
            value=100000,
        )

        create_discount_scope(
            discount=discount,
            variant=variant,
        )

        sync_variant_discount(
            variant=variant,
        )

        variant.refresh_from_db()

        self.assertEqual(
            variant.discount_amount,
            50000,
        )

        self.assertEqual(
            variant.final_price,
            0,
        )