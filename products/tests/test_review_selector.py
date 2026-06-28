from django.contrib.auth import get_user_model
from django.test import TestCase

from products.selectors import (
    get_product_reviews,
    get_review_by_id,
    get_user_review,
)

from products.tests.factories import (
    create_product,
)

from products.models import Review


User = get_user_model()


class ReviewSelectorTests(TestCase):

    def setUp(self):

        self.user1 = User.objects.create_user(
            phone_number="+989121111111",
            password="123456",
        )

        self.user2 = User.objects.create_user(
            phone_number="+989121111112",
            password="123456",
        )

        self.product = create_product()

    # =====================================================
    # get_product_reviews
    # =====================================================

    def test_get_product_reviews_returns_only_valid_reviews(self):

        review1 = Review.objects.create(
            product=self.product,
            user=self.user1,
            rating=5,
            comment="نظر اول",
            is_valid=True,
        )

        Review.objects.create(
            product=self.product,
            user=self.user2,
            rating=4,
            comment="نظر دوم",
            is_valid=False,
        )

        reviews = get_product_reviews(
            product_id=self.product.id,
        )

        self.assertEqual(
            reviews.count(),
            1,
        )

        self.assertEqual(
            reviews.first(),
            review1,
        )

    # =====================================================
    # get_review_by_id
    # =====================================================

    def test_get_review_by_id(self):

        review = Review.objects.create(
            product=self.product,
            user=self.user1,
            rating=5,
            comment="تست",
            is_valid=True,
        )

        result = get_review_by_id(
            review_id=review.id,
        )

        self.assertEqual(
            result,
            review,
        )

    # =====================================================
    # get_user_review
    # =====================================================

    def test_get_user_review(self):

        review = Review.objects.create(
            product=self.product,
            user=self.user1,
            rating=5,
            comment="نظر",
            is_valid=False,
        )

        result = get_user_review(
            product=self.product,
            user=self.user1,
        )

        self.assertEqual(
            result,
            review,
        )

    def test_get_user_review_other_user(self):

        Review.objects.create(
            product=self.product,
            user=self.user1,
            rating=5,
            comment="نظر",
            is_valid=True,
        )

        with self.assertRaises(Review.DoesNotExist):

            get_user_review(
                product=self.product,
                user=self.user2,
            )

    def test_get_user_review_invalid_review_is_returned(self):
        """
        حتی اگر نظر تایید نشده باشد، باید برای صاحب آن
        قابل دریافت باشد.
        """

        review = Review.objects.create(
            product=self.product,
            user=self.user1,
            rating=3,
            comment="در انتظار تایید",
            is_valid=False,
        )

        result = get_user_review(
            product=self.product,
            user=self.user1,
        )

        self.assertEqual(
            result,
            review,
        )