from django.db.models import Prefetch

from .constants import CartStatus
from .models import Cart, CartItem

from products.models import (
    ProductImage,
    ProductVariantAttribute,
    VariantImage,
)


def get_cart_queryset():
    """
    QuerySet بهینه برای نمایش سبد خرید.

    اطلاعات مورد نیاز Cart، Product، Variant، تصاویر،
    ویژگی‌ها و Propertyها از قبل بارگذاری می‌شوند
    تا از ایجاد N+1 Query جلوگیری شود.
    """

    primary_variant_images = Prefetch(
        "items__variant__images",
        queryset=VariantImage.objects.filter(
            is_primary=True,
        ),
        to_attr="primary_images",
    )

    primary_product_images = Prefetch(
        "items__variant__product__images",
        queryset=ProductImage.objects.filter(
            is_primary=True,
        ),
        to_attr="primary_images",
    )

    variant_attributes = Prefetch(
        "items__variant__attributes",
        queryset=(
            ProductVariantAttribute.objects
            .select_related(
                "attribute",
            )
            .prefetch_related(
                "properties",
            )
        ),
    )

    return (
        Cart.objects
        .select_related(
            "user",
            "coupon",
            "coupon__discount",
        )
        .prefetch_related(
            "items__variant__product__brand",
            "items__variant__product__category",
            primary_variant_images,
            primary_product_images,
            variant_attributes,
        )
    )


def get_user_active_cart(user):
    """
    دریافت سبد فعال کاربر.
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
    دریافت سبد فعال مهمان.
    """

    return (
        get_cart_queryset()
        .filter(
            session_key=session_key,
            status=CartStatus.ACTIVE,
        )
        .first()
    )


def get_cart_item_queryset():
    """
    QuerySet بهینه برای آیتم‌های سبد خرید.
    """

    primary_variant_images = Prefetch(
        "variant__images",
        queryset=VariantImage.objects.filter(
            is_primary=True,
        ),
        to_attr="primary_images",
    )

    primary_product_images = Prefetch(
        "variant__product__images",
        queryset=ProductImage.objects.filter(
            is_primary=True,
        ),
        to_attr="primary_images",
    )

    variant_attributes = Prefetch(
        "variant__variant_attributes",
        queryset=(
            ProductVariantAttribute.objects
            .select_related(
                "attribute",
            )
            .prefetch_related(
                "properties",
            )
        ),
    )

    return (
        CartItem.objects
        .select_related(
            "cart",
            "variant",
            "variant__product",
            "variant__product__brand",
            "variant__product__category",
        )
        .prefetch_related(
            primary_variant_images,
            primary_product_images,
            variant_attributes,
        )
    )


def get_cart_item_by_id(
    *,
    item_id,
    user=None,
    session_key=None,
):
    """
    دریافت آیتم سبد خرید بر اساس شناسه.

    فقط آیتم متعلق به سبد فعال کاربر یا مهمان
    برگردانده می‌شود.
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