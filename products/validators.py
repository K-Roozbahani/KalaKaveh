from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import (
    Product,
    ProductVariant,
    ProductAttributeValue,
)


def validate_product_is_active(
    *,
    product: Product,
) -> None:
    """
    بررسی فعال بودن محصول
    """

    if not product.is_active:
        raise ValidationError(
            _("محصول غیرفعال است.")
        )


def validate_variant_is_active(
    *,
    variant: ProductVariant,
) -> None:
    """
    بررسی فعال بودن تنوع محصول
    """

    if not variant.is_active:
        raise ValidationError(
            _("تنوع محصول غیرفعال است.")
        )

def validate_quantity(
    *,
    quantity: int,
):
    if quantity <= 0:
        raise ValidationError(
            _("تعداد باید بیشتر از صفر باشد.")
        )


def validate_variant_has_stock(
    *,
    variant: ProductVariant,
    quantity: int,
) -> None:
    """
    بررسی موجودی تنوع محصول
    """

    validate_quantity(quantity=quantity)

    if variant.stock < quantity:
        raise ValidationError(
            _("موجودی کافی نیست.")
        )


def validate_product_and_variant_are_active(
    *,
    variant: ProductVariant,
) -> None:
    """
    بررسی فعال بودن محصول و تنوع
    """

    validate_product_is_active(
        product=variant.product,
    )

    validate_variant_is_active(
        variant=variant,
    )


def validate_variant_can_be_purchased(
    *,
    variant: ProductVariant,
    quantity: int,
) -> None:
    """
    بررسی امکان خرید تنوع محصول
    """

    validate_product_and_variant_are_active(
        variant=variant,
    )

    validate_variant_has_stock(
        variant=variant,
        quantity=quantity,
    )

def validate_review_rating(
    *,
    rating: int,
) -> None:
    """
    اعتبارسنجی امتیاز محصول
    """

    if rating < 1 or rating > 5:
        raise ValidationError(
            _("امتیاز باید بین ۱ تا ۵ باشد.")
        )

def validate_attribute_value_belongs_to_product(
    *,
    variant: ProductVariant,
    attribute_value: ProductAttributeValue,
) -> None:
    """
    بررسی تعلق مقدار ویژگی به محصول تنوع
    """

    if attribute_value.product_id != variant.product_id:
        raise ValidationError(
            _("مقدار ویژگی متعلق به این محصول نیست.")
        )