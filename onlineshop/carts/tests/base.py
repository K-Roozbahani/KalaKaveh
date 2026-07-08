from rest_framework.test import APITestCase

from carts.services.cart import get_or_create_cart

from carts.tests.factories import (
    create_cart,
    create_cart_item,
)

from products.tests.factories import (
    create_variant,
)

from orders.tests.factories import (
    create_user,
)


class CartAPITestCase(APITestCase):
    """
    کلاس پایه برای تست‌های API سبد خرید
    """

    def create_session(self):
        """
        ایجاد Session برای کاربر مهمان
        """

        session = self.client.session
        session.save()

        return session.session_key

    def login(self, user=None):
        """
        لاگین کاربر
        """

        if user is None:
            user = create_user()

        self.client.force_authenticate(
            user=user,
        )

        return user

    def get_cart(self, user=None):
        """
        دریافت یا ایجاد سبد خرید
        """

        if user is not None:
            return get_or_create_cart(
                user=user,
            )

        return get_or_create_cart(
            session_key=self.create_session(),
        )

    def create_variant(self, **kwargs):
        """
        ایجاد Variant
        """

        return create_variant(**kwargs)

    def create_cart(self, **kwargs):
        """
        ایجاد Cart
        """

        return create_cart(**kwargs)

    def create_cart_item(self, **kwargs):
        """
        ایجاد CartItem
        """

        return create_cart_item(**kwargs)