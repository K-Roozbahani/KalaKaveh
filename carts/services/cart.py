from django.db import transaction

from carts.constants import CartStatus
from carts.models import (
    Cart,
    CartItem,
)

from products.services.stock import (
    ensure_variant_can_be_purchased,
)


def get_or_create_cart(
    *,
    user=None,
    session_key=None,
):
    """
    دریافت یا ایجاد سبد خرید فعال
    """

    if user is not None:
        cart, _ = Cart.objects.get_or_create(
            user=user,
            status=CartStatus.ACTIVE,
        )
        return cart

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
    افزودن کالا به سبد خرید
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
        ]
    )

    return item


@transaction.atomic
def update_cart_item(
    *,
    item,
    quantity,
):
    """
    بروزرسانی تعداد یک آیتم سبد خرید
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
    حذف یک آیتم از سبد خرید
    """

    item.delete()


@transaction.atomic
def clear_cart(
    *,
    cart,
):
    """
    حذف تمام آیتم‌های سبد خرید
    """

    cart.items.all().delete()

    return cart