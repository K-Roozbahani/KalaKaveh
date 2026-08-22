from django.db.models import Prefetch
from django.db.models import Sum

from .constants import CartStatus
from .models import (
    Cart,
    CartItem,
)

from products.models import (
    ProductImage,
    ProductVariantAttribute,
    VariantImage,
)


def get_cart_queryset():
    """
    QuerySet بهینه برای نمایش سبد خرید.

    اطلاعات مورد نیاز سبد خرید، محصول، تنوع محصول،
    تصاویر، ویژگی‌ها و Propertyها از قبل بارگذاری می‌شوند
    تا از ایجاد Queryهای اضافی و N+1 جلوگیری شود.
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


def get_user_active_cart(
    *,
    user,
):
    """
    دریافت سبد خرید فعال کاربر.

    اطلاعات مرتبط مورد نیاز برای نمایش سبد خرید
    نیز به صورت بهینه بارگذاری می‌شوند.
    """

    return (
        get_cart_queryset()
        .filter(
            user=user,
            status=CartStatus.ACTIVE,
        )
        .first()
    )


def get_guest_active_cart(
    *,
    session_key,
):
    """
    دریافت سبد خرید فعال مهمان بر اساس Session.
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

    اطلاعات Cart، Variant، Product، Brand، Category،
    تصاویر، ویژگی‌ها و Propertyهای ویژگی‌ها از قبل
    بارگذاری می‌شوند تا از N+1 Query جلوگیری شود.
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
        "variant__attributes",
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
    دریافت یک آیتم از سبد خرید فعال.

    آیتم فقط در صورتی برگردانده می‌شود که متعلق به
    سبد خرید فعال کاربر یا Session مهمان باشد.
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


def get_active_cart_item_count(
    *,
    user=None,
    session_key=None,
):
    """
    دریافت تعداد کل کالاهای موجود در سبد خرید فعال.

    مقدار quantity تمام آیتم‌های سبد خرید جمع می‌شود.
    در صورت نبودن سبد خرید یا خالی بودن آن، مقدار صفر برگردانده می‌شود.

    این Selector فقط برای خواندن اطلاعات استفاده می‌شود و
    هیچ سبد خرید جدیدی ایجاد نمی‌کند.
    """

    queryset = CartItem.objects.filter(
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

        return 0

    return (
        queryset
        .aggregate(
            total_quantity=Sum("quantity"),
        )
        .get("total_quantity")
        or 0
    )