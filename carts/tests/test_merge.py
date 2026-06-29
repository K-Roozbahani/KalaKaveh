from django.test import TestCase

from carts.services.merge import merge_guest_cart

from carts.tests.factories import (
    create_cart,
    create_cart_item,
)

from orders.tests.factories import create_user

from products.tests.factories import create_variant


class MergeGuestCartTests(TestCase):
    """
    تست سرویس ادغام سبد خرید مهمان
    """

    def test_move_item_to_user_cart(self):
        """
        در صورت نبود کالا در سبد کاربر،
        آیتم باید به سبد کاربر منتقل شود.
        """

        guest_cart = create_cart(
            session_key="guest-session",
        )

        user = create_user()

        user_cart = create_cart(
            user=user,
        )

        variant = create_variant(
            stock=10,
        )

        create_cart_item(
            cart=guest_cart,
            variant=variant,
            quantity=3,
        )

        merge_guest_cart(
            guest_cart=guest_cart,
            user_cart=user_cart,
        )

        self.assertEqual(
            user_cart.items.count(),
            1,
        )

        item = user_cart.items.first()

        self.assertEqual(
            item.variant,
            variant,
        )

        self.assertEqual(
            item.quantity,
            3,
        )

    def test_merge_same_variant(self):
        """
        اگر کالا در هر دو سبد باشد،
        تعداد آن‌ها با هم جمع می‌شود.
        """

        guest_cart = create_cart(
            session_key="guest-session",
        )

        user = create_user()

        user_cart = create_cart(
            user=user,
        )

        variant = create_variant(
            stock=10,
        )

        create_cart_item(
            cart=user_cart,
            variant=variant,
            quantity=2,
        )

        create_cart_item(
            cart=guest_cart,
            variant=variant,
            quantity=3,
        )

        merge_guest_cart(
            guest_cart=guest_cart,
            user_cart=user_cart,
        )

        item = user_cart.items.first()

        self.assertEqual(
            item.quantity,
            5,
        )

        self.assertEqual(
            user_cart.items.count(),
            1,
        )

    def test_quantity_should_not_exceed_stock(self):
        """
        تعداد نهایی نباید از موجودی کالا بیشتر شود.
        """

        guest_cart = create_cart(
            session_key="guest-session",
        )

        user = create_user()

        user_cart = create_cart(
            user=user,
        )

        variant = create_variant(
            stock=5,
        )

        create_cart_item(
            cart=user_cart,
            variant=variant,
            quantity=4,
        )

        create_cart_item(
            cart=guest_cart,
            variant=variant,
            quantity=3,
        )

        merge_guest_cart(
            guest_cart=guest_cart,
            user_cart=user_cart,
        )

        item = user_cart.items.first()

        self.assertEqual(
            item.quantity,
            5,
        )

    def test_remove_out_of_stock_item(self):
        """
        کالای بدون موجودی نباید به سبد کاربر منتقل شود.
        """

        guest_cart = create_cart(
            session_key="guest-session",
        )

        user = create_user()

        user_cart = create_cart(
            user=user,
        )

        variant = create_variant(
            stock=0,
        )

        create_cart_item(
            cart=guest_cart,
            variant=variant,
            quantity=2,
        )

        merge_guest_cart(
            guest_cart=guest_cart,
            user_cart=user_cart,
        )

        self.assertEqual(
            user_cart.items.count(),
            0,
        )

    def test_guest_cart_should_be_deleted(self):
        """
        پس از پایان عملیات،
        سبد مهمان باید حذف شود.
        """

        guest_cart = create_cart(
            session_key="guest-session",
        )

        guest_cart_id = guest_cart.id

        user = create_user()

        user_cart = create_cart(
            user=user,
        )

        variant = create_variant()

        create_cart_item(
            cart=guest_cart,
            variant=variant,
            quantity=1,
        )

        merge_guest_cart(
            guest_cart=guest_cart,
            user_cart=user_cart,
        )

        self.assertFalse(
            guest_cart.__class__.objects.filter(
                pk=guest_cart_id,
            ).exists()
        )