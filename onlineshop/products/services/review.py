from django.db import transaction
from django.utils.translation import gettext_lazy as _

from products.models import (
    Product,
    Review,
)
from products.validators import validate_review_rating, validate_review_comment, validate_review_can_be_updated


@transaction.atomic
def create_review(
    *,
    product: Product,
    user,
    rating: int,
    comment: str = "",
) -> Review:
    """
    ثبت یا بروزرسانی نظر کاربر
    """

    validate_review_rating(
        rating=rating,
    )

    validate_review_comment(
        comment=comment,
    )

    review, _ = Review.objects.update_or_create(
        product=product,
        user=user,
        defaults={
            "rating": rating,
            "comment": comment,
            "is_valid": False,
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
    ویرایش نظر
    """

    validate_review_can_be_updated(
        review=review,
    )

    validate_review_rating(
        rating=rating,
    )

    validate_review_comment(
        comment=comment,
    )

    review.rating = rating
    review.comment = comment
    review.is_valid = False

    review.save(
        update_fields=[
            "rating",
            "comment",
            "is_valid",
        ]
    )

    return review


@transaction.atomic
def deactivate_review(
    *,
    review: Review,
) -> Review:
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