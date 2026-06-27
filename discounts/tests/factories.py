from datetime import timedelta

from django.utils import timezone

from discounts.models import (
    Discount,
    DiscountScope,
    Coupon,
)

from products.tests.factories import (
    create_brand,
    create_category,
    create_product,
    create_variant,
)


def create_discount(**kwargs):
    """
    ساخت تخفیف تست
    """

    now = timezone.now()

    return Discount.objects.create(
        name=kwargs.get(
            "name",
            "تخفیف تست",
        ),
        discount_type=kwargs.get(
            "discount_type",
            Discount.PERCENT,
        ),
        value=kwargs.get(
            "value",
            10,
        ),
        priority=kwargs.get(
            "priority",
            100,
        ),
        is_active=kwargs.get(
            "is_active",
            True,
        ),
        start_date=kwargs.get(
            "start_date",
            now - timedelta(days=1),
        ),
        end_date=kwargs.get(
            "end_date",
            now + timedelta(days=1),
        ),
    )


def create_discount_scope(**kwargs):
    """
    ساخت Scope تست
    """

    discount = kwargs.pop(
        "discount",
        None,
    )

    if discount is None:
        discount = create_discount()

    variant = kwargs.pop(
        "variant",
        None,
    )

    product = kwargs.pop(
        "product",
        None,
    )

    category = kwargs.pop(
        "category",
        None,
    )

    brand = kwargs.pop(
        "brand",
        None,
    )

    if (
        variant is None and
        product is None and
        category is None and
        brand is None
    ):
        variant = create_variant()

    return DiscountScope.objects.create(
        discount=discount,
        target_type=kwargs.get(
            "target_type",
            4,
        ),
        variant=variant,
        product=product,
        category=category,
        brand=brand,
    )


def create_coupon(**kwargs):
    """
    ساخت کوپن تست
    """

    discount = kwargs.pop(
        "discount",
        None,
    )

    if discount is None:
        discount = create_discount()

    now = timezone.now()

    return Coupon.objects.create(
        code=kwargs.get(
            "code",
            "TEST10",
        ),
        discount=discount,
        usage_limit=kwargs.get(
            "usage_limit",
            1,
        ),
        used_count=kwargs.get(
            "used_count",
            0,
        ),
        is_active=kwargs.get(
            "is_active",
            True,
        ),
        start_date=kwargs.get(
            "start_date",
            now - timedelta(days=1),
        ),
        end_date=kwargs.get(
            "end_date",
            now + timedelta(days=1),
        ),
    )