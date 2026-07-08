from celery import shared_task

from products.models import ProductVariant
from discounts.services.discount import (
    refresh_variant_price,
)


@shared_task
def refresh_variant_price_task(variant_id: int):
    """
    بروزرسانی قیمت یک محصول (async)
    """

    try:
        variant = ProductVariant.objects.get(id=variant_id)
        refresh_variant_price(variant=variant)

    except ProductVariant.DoesNotExist:
        return "variant_not_found"


@shared_task
def refresh_all_variant_prices_task():
    """
    بروزرسانی کل قیمت‌ها (مثلاً بعد از تغییر Discount)
    """

    variants = ProductVariant.objects.select_related("product").all()

    for variant in variants:
        refresh_variant_price(variant=variant)

    return f"updated:{variants.count()}"


@shared_task
def refresh_product_variants_price_task(product_id: int):
    """
    بروزرسانی قیمت‌های یک محصول
    """

    variants = ProductVariant.objects.filter(
        product_id=product_id
    )

    for variant in variants:
        refresh_variant_price(variant=variant)

    return f"product:{product_id}_updated:{variants.count()}"