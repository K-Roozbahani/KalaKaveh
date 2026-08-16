from django.db import transaction

from carts.constants import CartStatus
from carts.models import (
    Cart,
    CartItem,
)

from carts.services.merge import (
    merge_guest_cart,
)

from products.services.stock import (
    ensure_variant_can_be_purchased,
)


@transaction.atomic
def get_or_create_cart(
    *,
    user=None,
    session_key=None,
):
    """
    دریافت یا ایجاد سبد خرید فعال.

    برای کاربر مهمان، سبد خرید بر اساس Session مدیریت می‌شود.

    برای کاربر احراز هویت‌شده، سبد خرید بر اساس User مدیریت می‌شود.
    در صورت وجود Session و Guest Cart مربوط به همان Session،
    سبد مهمان به سبد کاربر ادغام می‌شود.

    پس از ادغام، سبد کاربر دیگر به Session وابسته نخواهد بود.
    """

    if user is not None:

        user_cart, _ = (
            Cart.objects
            .select_for_update()
            .get_or_create(
                user=user,
                status=CartStatus.ACTIVE,
                defaults={
                    "session_key": None,
                },
            )
        )

        # -------------------------------------------------
        # پاک‌سازی Session از سبد کاربر
        #
        # پس از احراز هویت، مالک سبد User است و دیگر
        # نباید به Session وابسته باشد.
        # -------------------------------------------------

        if user_cart.session_key is not None:

            user_cart.session_key = None

            user_cart.save(
                update_fields=[
                    "session_key",
                    "updated_at",
                ],
            )

        # -------------------------------------------------
        # Lazy Merge
        #
        # فقط Guest Cart مربوط به Session فعلی بررسی می‌شود.
        # Cartهای Sessionهای دیگر کاربر دست‌نخورده باقی می‌مانند.
        # -------------------------------------------------

        if session_key:

            guest_cart = (
                Cart.objects
                .select_for_update()
                .filter(
                    session_key=session_key,
                    status=CartStatus.ACTIVE,
                )
                .first()
            )

            if guest_cart is not None:

                merge_guest_cart(
                    guest_cart=guest_cart,
                    user_cart=user_cart,
                )

        return user_cart

    # -----------------------------------------------------
    # Guest Cart
    # -----------------------------------------------------

    if not session_key:
        raise ValueError(
            "session_key برای ایجاد سبد خرید مهمان الزامی است."
        )

    cart, _ = Cart.objects.get_or_create(
        session_key=session_key,
        status=CartStatus.ACTIVE,
    )

    return cart


@transaction.atomic
def add_to_cart(
    *,
    cart,
    variant,
    quantity,
):
    """
    افزودن کالا به سبد خرید.
    """

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        variant=variant,
        defaults={
            "quantity": quantity,
        },
    )

    if created:

        ensure_variant_can_be_purchased(
            variant=variant,
            quantity=quantity,
        )

        return item

    new_quantity = item.quantity + quantity

    ensure_variant_can_be_purchased(
        variant=variant,
        quantity=new_quantity,
    )

    item.quantity = new_quantity

    item.save(
        update_fields=[
            "quantity",
            "updated_at",
        ],
    )

    return item


@transaction.atomic
def update_cart_item(
    *,
    item,
    quantity,
):
    """
    بروزرسانی تعداد یک آیتم سبد خرید.
    """

    ensure_variant_can_be_purchased(
        variant=item.variant,
        quantity=quantity,
    )

    item.quantity = quantity

    item.save(
        update_fields=[
            "quantity",
            "updated_at",
        ],
    )

    return item


@transaction.atomic
def remove_cart_item(
    *,
    item,
):
    """
    حذف یک آیتم از سبد خرید.
    """

    item.delete()


@transaction.atomic
def clear_cart(
    *,
    cart,
):
    """
    حذف تمام آیتم‌های سبد خرید.
    """

    cart.items.all().delete()

    return cart