from django.db import transaction

from discounts.models import (
    Discount,
)

from discounts.selectors import (
    get_highest_priority_discount,
)

from discounts.validators import (
    validate_price,
    validate_discount_amount,
    validate_final_price,
)

from products.models import (
    ProductVariant,
)


def calculate_discount_amount(
    *,
    price: int,
    discount: Discount,
) -> int:
    """
    محاسبه مبلغ تخفیف
    """

    validate_price(
        price=price,
    )

    if discount.discount_type == Discount.PERCENT:

        amount = (
            price *
            discount.value
        ) // 100

    elif discount.discount_type == Discount.FIXED:

        amount = min(
            discount.value,
            price,
        )

    else:
        amount = 0

    validate_discount_amount(
        discount_amount=amount,
        price=price,
    )

    return amount


def calculate_variant_price(
    *,
    variant: ProductVariant,
) -> dict:
    """
    محاسبه قیمت نهایی تنوع محصول

    خروجی:

    {
        "price": 1000000,
        "discount_amount": 100000,
        "final_price": 900000,
        "discount": discount_instance,
    }
    """

    price = variant.price

    discount_scope = (
        get_highest_priority_discount(
            variant=variant,
        )
    )

    if not discount_scope:

        return {
            "price": price,
            "discount_amount": 0,
            "final_price": price,
            "discount": None,
        }

    discount = discount_scope.discount

    discount_amount = calculate_discount_amount(
        price=price,
        discount=discount,
    )

    final_price = (
        price -
        discount_amount
    )

    validate_final_price(
        final_price=final_price,
    )

    return {
        "price": price,
        "discount_amount": discount_amount,
        "final_price": final_price,
        "discount": discount,
    }


@transaction.atomic
def refresh_variant_price(
    *,
    variant: ProductVariant,
) -> ProductVariant:
    """
    بروزرسانی کش قیمت تنوع محصول
    """

    pricing = calculate_variant_price(
        variant=variant,
    )

    variant.discount_amount = pricing[
        "discount_amount"
    ]

    variant.final_price = pricing[
        "final_price"
    ]

    variant.save(
        update_fields=[
            "discount_amount",
            "final_price",
        ]
    )

    return variant


@transaction.atomic
def refresh_variants_prices(
    *,
    queryset,
) -> int:
    """
    بروزرسانی گروهی قیمت تنوع‌ها

    خروجی:
        تعداد رکوردهای بروزرسانی شده
    """

    updated_count = 0

    for variant in queryset:

        refresh_variant_price(
            variant=variant,
        )

        updated_count += 1

    return updated_count