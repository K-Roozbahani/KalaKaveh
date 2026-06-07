from django.utils import timezone

from discounts.models import Discount


def get_variant_discount(variant):
    """
    مقدار تخفیف اعمال‌شده روی Variant را برمی‌گرداند.
    """

    now = timezone.now()

    discounts = (
        Discount.objects.filter(
            is_active=True,
            start_date__lte=now,
            end_date__gte=now,
        )
        .prefetch_related("targets")
        .order_by("-priority")
    )

    for discount in discounts:

        target_exists = (
            discount.targets.filter(variant=variant).exists()
            or
            discount.targets.filter(product=variant.product).exists()
            or
            (
                variant.product.category and
                discount.targets.filter(
                    category=variant.product.category
                ).exists()
            )
            or
            (
                variant.product.brand and
                discount.targets.filter(
                    brand=variant.product.brand
                ).exists()
            )
        )

        if not target_exists:
            continue

        if discount.discount_type == Discount.PERCENT:
            return (variant.price * discount.value) // 100

        return min(discount.value, variant.price)

    return 0
