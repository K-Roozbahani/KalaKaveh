from django.db import transaction

from carts.models import CartItem


@transaction.atomic
def merge_guest_cart(
    *,
    guest_cart,
    user_cart,
):
    """
    ادغام سبد خرید مهمان با سبد خرید کاربر.

    اگر یک کالا در هر دو سبد وجود داشته باشد،
    تعداد آن‌ها با هم جمع می‌شود اما از موجودی
    فعلی کالا بیشتر نخواهد شد.

    کالاهای بدون موجودی از سبد مهمان حذف می‌شوند.
    """

    guest_items = guest_cart.items.select_related(
        "variant",
    )

    for guest_item in guest_items:

        variant = guest_item.variant

        if variant.stock <= 0:
            guest_item.delete()
            continue

        user_item = CartItem.objects.filter(
            cart=user_cart,
            variant=variant,
        ).first()

        if user_item is None:

            guest_item.cart = user_cart
            guest_item.quantity = min(
                guest_item.quantity,
                variant.stock,
            )

            guest_item.save(
                update_fields=[
                    "cart",
                    "quantity",
                ],
            )

            continue

        user_item.quantity = min(
            user_item.quantity +
            guest_item.quantity,
            variant.stock,
        )

        user_item.save(
            update_fields=[
                "quantity",
                "updated_at",
            ],
        )

        guest_item.delete()

    guest_cart.delete()

    return user_cart