from django.db import transaction
from django.utils.translation import gettext_lazy as _

from products.models import (
    Product,
    Review,
)


@transaction.atomic
def create_review(
    *,
    product: Product,
    user,
    rating: int,
    comment: str = "",
) -> Review:
    """
    ثبت نظر برای محصول

    اگر کاربر قبلاً نظری ثبت کرده باشد،
    همان نظر بروزرسانی می‌شود.
    """

    review, _ = Review.objects.update_or_create(
        product=product,
        user=user,
        defaults={
            "rating": rating,
            "comment": comment,
        },
    )

    return review


@transaction.atomic
def update_review(
    *,
    review: Review,
    rating: int,
    comment: str,
) -> Review:
    """
    بروزرسانی نظر
    """

    review.rating = rating
    review.comment = comment

    review.is_valid = False

    review.save(
        update_fields=[
            "rating",
            "comment",
        ],
    )

    return review


@transaction.atomic
def deactivate_review(
    *,
    review: Review,
):
    """
    حذف منطقی نظر
    """

    review.comment = _("[**توسط کاربر حذف شد**]\n\n")

    review.is_valid = False

    review.save(
        update_fields=[
            "comment",
            "is_valid",
        ],
    )

    return review