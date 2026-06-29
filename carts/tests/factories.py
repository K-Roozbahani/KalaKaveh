from carts.models import (
    Cart,
    CartItem,
)

from carts.constants import CartStatus


def create_cart(
    *,
    user=None,
    session_key=None,
    status=CartStatus.ACTIVE,
):
    """
    ایجاد سبد خرید
    """

    return Cart.objects.create(
        user=user,
        session_key=session_key,
        status=status,
    )


def create_cart_item(
    *,
    cart,
    variant,
    quantity=1,
):
    """
    ایجاد آیتم سبد خرید
    """

    return CartItem.objects.create(
        cart=cart,
        variant=variant,
        quantity=quantity,
    )