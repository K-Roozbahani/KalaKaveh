"""
Dispatcher جهت فراخوانی Task های Celery

هدف این فایل حذف وابستگی مستقیم Service ها به Task ها است.
"""

from discounts.tasks import (
    refresh_all_variant_prices_task,
    refresh_product_variants_price_task,
    refresh_variant_price_task,
)


def refresh_variant_price(
    variant_id: int,
) -> None:
    """
    بروزرسانی قیمت یک Variant
    """

    refresh_variant_price_task.delay(
        variant_id=variant_id,
    )


def refresh_product_variants_price(
    product_id: int,
) -> None:
    """
    بروزرسانی قیمت تمام Variant های یک محصول
    """

    refresh_product_variants_price_task.delay(
        product_id=product_id,
    )


def refresh_all_variant_prices() -> None:
    """
    بروزرسانی قیمت تمام Variant ها
    """

    refresh_all_variant_prices_task.delay()