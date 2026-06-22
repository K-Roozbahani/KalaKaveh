from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Product, ProductVariant, ProductAttributeValue


def validate_product_is_active(*, product: Product) -> None:
    if not product.is_active:
        raise ValidationError(_("محصول غیرفعال است."))


def validate_variant_is_active(*, variant: ProductVariant) -> None:
    if not variant.is_active:
        raise ValidationError(_("تنوع محصول غیرفعال است."))


def validate_quantity(*, quantity: int) -> None:
    if quantity <= 0:
        raise ValidationError(_("تعداد باید بیشتر از صفر باشد."))


def validate_variant_has_stock(
    *,
    variant: ProductVariant,
    quantity: int,
) -> None:
    validate_quantity(quantity=quantity)

    if variant.stock < quantity:
        raise ValidationError(_("موجودی کافی نیست."))


def validate_review_rating(*, rating: int) -> None:
    if rating < 1 or rating > 5:
        raise ValidationError(_("امتیاز باید بین ۱ تا ۵ باشد."))


def validate_attribute_value_belongs_to_product(
    *,
    variant: ProductVariant,
    attribute_value: ProductAttributeValue,
) -> None:
    if attribute_value.product_id != variant.product_id:
        raise ValidationError(_("مقدار ویژگی متعلق به این محصول نیست."))