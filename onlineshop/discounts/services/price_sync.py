from products.models import ProductVariant

from discounts.services.price_engine import (
    calculate_variant_price,
)


def sync_variant_discount(
    *,
    variant: ProductVariant,
) -> ProductVariant:
    """
    بروزرسانی Snapshot قیمت تنوع محصول

    مسئولیت:
        - دریافت Snapshot از Price Engine
        - ذخیره Snapshot در دیتابیس

    مسئولیتی ندارد:
        - محاسبه تخفیف
        - انتخاب Discount
        - محاسبه قیمت نهایی
    """

    snapshot = calculate_variant_price(
        variant=variant,
    )

    variant.discount_amount = (
        snapshot.discount_amount
    )

    variant.final_price = (
        snapshot.final_price
    )

    variant.save(
        update_fields=[
            "discount_amount",
            "final_price",
        ],
    )

    return variant