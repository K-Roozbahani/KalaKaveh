from dataclasses import dataclass

from discounts.models import (
    Discount,
    DiscountScope,
)
from discounts.selectors import (
    get_highest_priority_discount,
)

from products.models import ProductVariant


@dataclass(frozen=True)
class PriceSnapshot:
    """
    نتیجه محاسبه قیمت یک تنوع محصول
    """

    base_price: int

    discount_amount: int

    final_price: int

    discount: Discount | None

    scope: DiscountScope | None


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


def calculate_variant_price(
    *,
    variant: ProductVariant,
) -> PriceSnapshot:
    """
    محاسبه قیمت نهایی تنوع محصول

    این سرویس هیچ تغییری در دیتابیس ایجاد نمی‌کند
    و فقط Snapshot قیمت را برمی‌گرداند.
    """

    scope = get_highest_priority_discount(
        variant=variant,
    )

    if scope is None:

        return PriceSnapshot(
            base_price=variant.price,
            discount_amount=0,
            final_price=variant.price,
            discount=None,
            scope=None,
        )

    discount = scope.discount

    discount_amount = calculate_discount_amount(
        price=variant.price,
        discount=discount,
    )

    final_price = max(
        variant.price - discount_amount,
        0,
    )

    return PriceSnapshot(
        base_price=variant.price,
        discount_amount=discount_amount,
        final_price=final_price,
        discount=discount,
        scope=scope,
    )