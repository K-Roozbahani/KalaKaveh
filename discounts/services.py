from django.db.models import Q
from django.utils import timezone

from discounts.models import DiscountTarget, Discount


def get_variant_discount(variant):
    """
    مقدار تخفیف اعمال شده روی یک Variant
    """

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
        .order_by("-discount__priority", "-target_type")
        .first()
    )

    if not target:
        return 0

    discount = target.discount

    if discount.discount_type == Discount.PERCENT:
        return (variant.price * discount.value) // 100

    return min(discount.value, variant.price)