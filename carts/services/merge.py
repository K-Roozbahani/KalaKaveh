from django.db import transaction

from carts.models import CartItem


@transaction.atomic
def merge_guest_cart(
    *,
    guest_cart,
    user_cart,
):
    """
    ادغام سبد مهمان با سبد کاربر
    """

    for item in guest_cart.items.all():

        existing = (
            user_cart.items
            .filter(
                variant=item.variant
            )
            .first()
        )

        if existing:

            existing.quantity += item.quantity

            existing.save(
                update_fields=[
                    "quantity"
                ]
            )

        else:

            CartItem.objects.create(
                cart=user_cart,
                variant=item.variant,
                quantity=item.quantity,
            )

    guest_cart.delete()

    return user_cart