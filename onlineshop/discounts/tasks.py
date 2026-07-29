"""
تسک‌های Celery مربوط به مدیریت تخفیف‌ها
"""

import logging

from celery import shared_task

from discounts.services.discount import refresh_variant_price
from products.models import ProductVariant
from utils.celery.base import BaseTask

# Logger اختصاصی Celery
logger = logging.getLogger("celery")


@shared_task(
    base=BaseTask,
    name="discounts.refresh_variant_price",
    queue="maintenance",
)
def refresh_variant_price_task(variant_id: int):
    """
    بروزرسانی قیمت یک Variant
    """

    try:
        variant = ProductVariant.objects.get(
            pk=variant_id,
        )

    except ProductVariant.DoesNotExist:

        logger.warning(
            "Variant یافت نشد.",
            extra={
                "variant_id": variant_id,
            },
        )

        return "variant_not_found"

    refresh_variant_price(
        variant=variant,
    )

    logger.info(
        "قیمت Variant بروزرسانی شد.",
        extra={
            "variant_id": variant_id,
        },
    )

    return "success"


@shared_task(
    base=BaseTask,
    name="discounts.refresh_product_variants_price",
    queue="maintenance",
)
def refresh_product_variants_price_task(
    product_id: int,
):
    """
    بروزرسانی قیمت تمام Variant های یک محصول
    """

    variants = ProductVariant.objects.filter(
        product_id=product_id,
    )

    updated = 0

    for variant in variants:

        refresh_variant_price(
            variant=variant,
        )

        updated += 1

    logger.info(
        "قیمت Variant های محصول بروزرسانی شد.",
        extra={
            "product_id": product_id,
            "updated": updated,
        },
    )

    return f"updated:{updated}"


@shared_task(
    base=BaseTask,
    name="discounts.refresh_all_variant_prices",
    queue="maintenance",
)
def refresh_all_variant_prices_task():
    """
    بروزرسانی قیمت تمام Variant ها

    این Task توسط Celery Beat اجرا می‌شود.
    """

    variants = ProductVariant.objects.select_related(
        "product",
    )

    updated = 0

    for variant in variants.iterator(
        chunk_size=500,
    ):

        refresh_variant_price(
            variant=variant,
        )

        updated += 1

    logger.info(
        "بروزرسانی قیمت تمام Variant ها پایان یافت.",
        extra={
            "updated": updated,
        },
    )

    return f"updated:{updated}"