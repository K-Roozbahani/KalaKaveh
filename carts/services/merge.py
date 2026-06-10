from django.db import transaction

from carts.models import CartItem


@transaction.atomic
def merge_guest_cart(*, guest_cart, user_cart):
    """
    ادغام سبد مهمان با سبد کاربر.

    در صورت وجود کالا در هر دو سبد، تعدادها با هم
    جمع می‌شوند اما از موجودی کالا بیشتر نخواهند شد.
    """

    guest_items = guest_cart.items.select_related(
        "variant",
    )

    for guest_item in guest_items:

        user_item = CartItem.objects.filter(
            cart=user_cart,
            variant=guest_item.variant,
        ).first()

        if guest_item.variant.stock <= 0:
            guest_item.delete()

            continue

        if not user_item:

            quantity = min(
                guest_item.quantity,
                guest_item.variant.stock,
            )

            guest_item.cart = user_cart
            guest_item.quantity = quantity

            guest_item.save(
                update_fields=[
                    "cart",
                    "quantity",
                ],
            )

            continue

        merged_quantity = (
            user_item.quantity
            + guest_item.quantity
        )

        merged_quantity = min(
            merged_quantity,
            guest_item.variant.stock,
        )

        user_item.quantity = merged_quantity

        user_item.save(
            update_fields=["quantity"],
        )

        guest_item.delete()

    guest_cart.delete()

    return user_cart