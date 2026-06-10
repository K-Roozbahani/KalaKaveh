from django.db import transaction

from carts.models import Cart, CartItem

from carts.services.validators import validate_variant_availability



def get_or_create_cart(
    *,
    user=None,
    session_key=None,
):
    """
    دریافت یا ساخت سبد فعال
    """

    if user:
        cart, _ = Cart.objects.get_or_create(
            user=user,
            status=Cart.Status.ACTIVE,
        )
        return cart

    cart, _ = Cart.objects.get_or_create(
        session_key=session_key,
        status=Cart.Status.ACTIVE,
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
    افزودن محصول به سبد
    """

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        variant=variant,
        defaults={
            "quantity": quantity,
        },
    )

    if created:
        validate_variant_availability(
            variant=variant,
            quantity=quantity,
        )

        return item

    new_quantity = item.quantity + quantity

    validate_variant_availability(
        variant=variant,
        quantity=new_quantity,
    )

    item.quantity = new_quantity

    item.save(update_fields=["quantity"])

    return item


@transaction.atomic
def update_cart_item(
    *,
    item,
    quantity,
):
    """
    تغییر تعداد
    """
    validate_variant_availability(
        variant=item.variant,
        quantity=quantity,
    )

    item.quantity = quantity

    item.save(
        update_fields=[
            "quantity",
            "updated_at",
        ]
    )

    return item


@transaction.atomic
def remove_cart_item(item):
    """
    حذف آیتم
    """

    item.delete()


def clear_cart(*, cart: Cart):
    """
    حذف تمام آیتم‌های سبد خرید.
    """

    cart.items.all().delete()

    cart.coupon = None

    cart.save(update_fields=["coupon"])

    return cart