from decimal import Decimal

from discounts.models import (
    Discount,
    DiscountScope,
)
from products.models import ProductVariant


def get_variant_active_discount(
    *,
    variant: ProductVariant,
):
    """
    دریافت بهترین تخفیف فعال برای تنوع محصول
    """

    discounts = Discount.objects.filter(
        is_active=True,
        scopes__variant=variant,
    ).order_by(
        "-priority",
    )

    return discounts.first()


def calculate_discount_amount(
    *,
    price: int,
    discount: Discount,
) -> int:
    """
    محاسبه مبلغ تخفیف
    """

    if discount.discount_type == Discount.PERCENT:

        return int(
            price *
            discount.value /
            100
        )

    return min(
        discount.value,
        price,
    )


def apply_discount_to_variant(
    *,
    variant: ProductVariant,
    discount: Discount | None,
) -> ProductVariant:
    """
    اعمال تخفیف روی تنوع محصول
    """

    if discount is None:

        variant.discount_amount = 0

        variant.final_price = (
            variant.price
        )

        variant.save(
            update_fields=[
                "discount_amount",
                "final_price",
            ]
        )

        return variant

    discount_amount = calculate_discount_amount(
        price=variant.price,
        discount=discount,
    )

    variant.discount_amount = (
        discount_amount
    )

    variant.final_price = max(
        variant.price -
        discount_amount,
        0,
    )

    variant.save(
        update_fields=[
            "discount_amount",
            "final_price",
        ]
    )

    return variant


def sync_variant_discount(
    *,
    variant: ProductVariant,
):
    """
    بروزرسانی قیمت تنوع محصول
    """

    discount = get_variant_active_discount(
        variant=variant,
    )

    return apply_discount_to_variant(
        variant=variant,
        discount=discount,
    )


