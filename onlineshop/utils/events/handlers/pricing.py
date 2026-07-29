"""
Handler های Event مربوط به Price Engine
"""

from discounts.tasks import (
    refresh_all_variant_prices_task,
    refresh_product_variants_price_task,
    refresh_variant_price_task,
)


def handle_variant_updated(
    variant_id: int,
) -> None:
    """
    مدیریت تغییر یک Variant
    """

    refresh_variant_price_task.delay(
        variant_id=variant_id,
    )


def handle_product_updated(
    product_id: int,
) -> None:
    """
    مدیریت تغییر یک Product
    """

    refresh_product_variants_price_task.delay(
        product_id=product_id,
    )


def handle_discount_updated() -> None:
    """
    مدیریت تغییر Discount
    """

    refresh_all_variant_prices_task.delay()