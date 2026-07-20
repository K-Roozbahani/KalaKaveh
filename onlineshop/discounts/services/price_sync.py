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

    updated_fields = []

    if variant.discount_amount != snapshot.discount_amount:
        variant.discount_amount = snapshot.discount_amount
        updated_fields.append("discount_amount")

    if variant.final_price != snapshot.final_price:
        variant.final_price = snapshot.final_price
        updated_fields.append("final_price")

    if updated_fields:
        variant.save(update_fields=updated_fields)

    return variant