from django.db.models import Prefetch

from .constants import CartStatus
from .models import Cart


def get_cart_queryset():
    """
    Queryset بهینه برای نمایش سبد خرید
    """

    return (
        Cart.objects.select_related(
            "user",
            "coupon",
            "coupon__discount",
        )
        .prefetch_related(
            "items",
            "items__variant",
            "items__variant__product",
            "items__variant__product__brand",
            "items__variant__product__category",
        )
    )


def get_user_active_cart(user):
    """
    دریافت سبد فعال کاربر
    """

    return (
        get_cart_queryset()
        .filter(
            user=user,
            status=CartStatus.ACTIVE,
        )
        .first()
    )


def get_guest_active_cart(session_key):
    """
    دریافت سبد فعال مهمان
    """

    return (
        get_cart_queryset()
        .filter(
            session_key=session_key,
            status=Cart.Status.ACTIVE,
        )
        .first()
    )


from carts.constants import CartStatus
from carts.models import CartItem


def get_cart_item_queryset():
    """
    QuerySet بهینه برای آیتم‌های سبد خرید
    """

    return (
        CartItem.objects.select_related(
            "cart",
            "variant",
            "variant__product",
            "variant__product__brand",
            "variant__product__category",
        )
    )


def get_cart_item_by_id(
    *,
    item_id,
    user=None,
    session_key=None,
):
    """
    دریافت آیتم سبد خرید بر اساس شناسه

    فقط در صورتی آیتم برگردانده می‌شود که
    متعلق به سبد خرید فعال کاربر یا مهمان باشد.
    """

    queryset = get_cart_item_queryset().filter(
        id=item_id,
        cart__status=CartStatus.ACTIVE,
    )

    if user is not None:

        queryset = queryset.filter(
            cart__user=user,
        )

    elif session_key is not None:

        queryset = queryset.filter(
            cart__session_key=session_key,
        )

    else:
        return None

    return queryset.first()