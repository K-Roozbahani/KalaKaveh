from django.core.exceptions import ValidationError

from carts.models import Cart
from carts.constants import CartStatus


def validate_cart_exists(cart):
    if cart is None:
        raise ValidationError("سبد خرید یافت نشد.")


def validate_cart_status(cart):
    if cart.status != CartStatus.ACTIVE:
        raise ValidationError("سبد خرید فعال نیست.")


def validate_cart_not_empty(cart):
    if not cart.items.exists():
        raise ValidationError("سبد خرید خالی است.")


def validate_address_owner(address, user):
    if address.user_id != user.id:
        raise ValidationError("آدرس متعلق به کاربر نیست.")


def validate_variant_stock(variant, quantity):
    if variant.stock < quantity:
        raise ValidationError(
            f"موجودی محصول {variant} کافی نیست."
        )


def validate_cart_stock(cart):
    for item in cart.items.select_related("variant"):
        validate_variant_stock(
            item.variant,
            item.quantity,
        )