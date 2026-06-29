from django.db import transaction

from products.models import (
    ProductImage,
    VariantImage,
)


# =====================================================
# Product Images
# =====================================================

@transaction.atomic
def set_primary_product_image(
    *,
    image: ProductImage,
) -> ProductImage:
    """
    تعیین تصویر اصلی محصول
    """

    (
        ProductImage.objects
        .filter(
            product=image.product,
            is_primary=True,
        )
        .exclude(
            pk=image.pk,
        )
        .update(
            is_primary=False,
        )
    )

    image.is_primary = True

    image.save(
        update_fields=[
            "is_primary",
        ],
    )

    return image


# =====================================================
# Variant Images
# =====================================================

@transaction.atomic
def set_primary_variant_image(
    *,
    image: VariantImage,
) -> VariantImage:
    """
    تعیین تصویر اصلی تنوع محصول
    """

    (
        VariantImage.objects
        .filter(
            variant=image.variant,
            is_primary=True,
        )
        .exclude(
            pk=image.pk,
        )
        .update(
            is_primary=False,
        )
    )

    image.is_primary = True

    image.save(
        update_fields=[
            "is_primary",
        ],
    )

    return image