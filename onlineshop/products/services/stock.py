from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from products.models import ProductVariant
from products.validators import (
    validate_quantity,
    validate_product_is_active, validate_variant_is_active, validate_variant_has_stock,
)

def ensure_variant_can_be_purchased(*, variant, quantity):
    """
    بررسی کامل امکان خرید
    """

    validate_product_is_active(
        product=variant.product,
    )

    validate_variant_is_active(
        variant=variant,
    )

    validate_variant_has_stock(
        variant=variant,
        quantity=quantity,
    )

    return True

@transaction.atomic
def decrease_stock(
    *,
    variant: ProductVariant,
    quantity: int,
) -> ProductVariant:
    """
    کاهش موجودی تنوع محصول

    استفاده:
    - ساخت سفارش
    - تبدیل سبد خرید به سفارش
    """

    variant = (
        ProductVariant.objects
        .select_for_update()
        .select_related("product")
        .get(pk=variant.pk)
    )

    ensure_variant_can_be_purchased(
        variant=variant,
        quantity=quantity,
    )

    variant.stock -= quantity

    variant.save(
        update_fields=["stock"],
    )

    return variant


@transaction.atomic
def increase_stock(
    *,
    variant: ProductVariant,
    quantity: int,
) -> ProductVariant:
    """
    افزایش موجودی

    استفاده:
    - لغو سفارش
    - بازگشت وجه
    """

    validate_quantity(quantity=quantity)

    variant = (
        ProductVariant.objects
        .select_for_update()
        .get(pk=variant.pk)
    )

    variant.stock += quantity

    variant.save(
        update_fields=["stock"],
    )

    return variant


@transaction.atomic
def set_stock(
    *,
    variant: ProductVariant,
    quantity: int,
) -> ProductVariant:
    """
    تنظیم مستقیم موجودی

    استفاده:
    - پنل مدیریت
    - عملیات انبارگردانی
    """

    if quantity < 0:
        raise ValidationError(
            _("موجودی نمی‌تواند منفی باشد.")
        )

    variant = (
        ProductVariant.objects
        .select_for_update()
        .get(pk=variant.pk)
    )

    variant.stock = quantity

    variant.save(
        update_fields=["stock"],
    )

    return variant