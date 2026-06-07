from django.db.models import Q
from django.utils import timezone

from products.models import ProductVariant
from discounts.models import (
    Discount,
    DiscountTarget
)


#سرویس محاسبه تخفیف
def calculate_discount_for_variant(variant):

    now = timezone.now()

    target = (
        DiscountTarget.objects
        .filter(
            Q(variant=variant) |
            Q(product=variant.product) |
            Q(category=variant.product.category) |
            Q(brand=variant.product.brand),

            discount__is_active=True,
            discount__start_date__lte=now,
            discount__end_date__gte=now,
        )
        .select_related("discount")
        .order_by("-discount__priority")
        .first()
    )

    if not target:
        return 0

    discount = target.discount

    if discount.discount_type == Discount.PERCENT:
        return (variant.price * discount.value) // 100

    return min(
        discount.value,
        variant.price
    )


#سرویس بروزرسانی Variant
def update_variant_discount(variant):

    amount = calculate_discount_for_variant(
        variant
    )

    variant.discount_amount = amount

    variant.final_price = (
        variant.price - amount
    )

    variant.save(
        update_fields=[
            "discount_amount",
            "final_price",
        ]
    )


# بروزرسانی گروهی
def update_discount_variants(
    discount
):
    """
    پس از ایجاد یا ویرایش تخفیف
    """

    variants = set()

    for target in discount.targets.all():

        if target.variant:
            variants.add(target.variant)

        elif target.product:
            variants.update(
                target.product.variants.all()
            )

        elif target.category:
            variants.update(
                target.category.products
                .prefetch_related(
                    "variants"
                )
                .values_list(
                    "variants__id",
                    flat=True
                )
            )

        elif target.brand:
            variants.update(
                target.brand.products
                .prefetch_related(
                    "variants"
                )
                .values_list(
                    "variants__id",
                    flat=True
                )
            )

    return variants


def get_discount_variants(discount):

    query = Q()

    for target in discount.targets.all():

        if target.variant_id:
            query |= Q(
                id=target.variant_id
            )

        elif target.product_id:
            query |= Q(
                product_id=target.product_id
            )

        elif target.category_id:
            query |= Q(
                product__category_id=target.category_id
            )

        elif target.brand_id:
            query |= Q(
                product__brand_id=target.brand_id
            )

    return ProductVariant.objects.filter(
        query
    ).distinct()

def refresh_discount_prices(discount):

    variants = get_discount_variants(discount)

    for variant in variants:
        update_variant_discount(variant)

