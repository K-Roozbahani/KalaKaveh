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