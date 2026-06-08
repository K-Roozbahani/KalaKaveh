from django.db.models import Prefetch

from .models import Cart, CartItem


def get_cart_queryset():
    """
    Queryset بهینه برای نمایش سبد خرید
    """

    return (
        Cart.objects
        .select_related(
            "user",
            "coupon",
        )
        .prefetch_related(
            Prefetch(
                "items",
                queryset=CartItem.objects.select_related(
                    "variant",
                    "variant__product",
                )
            )
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
            status=Cart.Status.ACTIVE,
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