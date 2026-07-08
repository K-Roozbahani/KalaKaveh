from django.contrib.auth import get_user_model
from django.test import TestCase

from products.models import Review
from products.services.review import (
    create_review,
    update_review,
    deactivate_review,
)
from products.tests.factories import (
    create_product,
)

User = get_user_model()


class ReviewServiceTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            phone_number="+989121111111",
            password="123456",
        )

        self.product = create_product()

    def test_create_review(self):
        """
        ثبت نظر جدید
        """

        review = create_review(
            product=self.product,
            user=self.user,
            rating=5,
            comment="نظر تست",
        )

        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "نظر تست")
        self.assertFalse(review.is_valid)

    def test_create_review_updates_existing_review(self):
        """
        ثبت مجدد، نظر قبلی را بروزرسانی می‌کند.
        """

        create_review(
            product=self.product,
            user=self.user,
            rating=5,
            comment="نظر اول",
        )

        review = create_review(
            product=self.product,
            user=self.user,
            rating=3,
            comment="نظر دوم",
        )

        self.assertEqual(
            Review.objects.count(),
            1,
        )

        self.assertEqual(review.rating, 3)
        self.assertEqual(review.comment, "نظر دوم")
        self.assertFalse(review.is_valid)

    def test_update_review(self):
        """
        بروزرسانی نظر
        """

        review = create_review(
            product=self.product,
            user=self.user,
            rating=5,
            comment="نظر اولیه",
        )

        review.is_valid = True
        review.save(update_fields=["is_valid"])

        review = update_review(
            review=review,
            rating=2,
            comment="ویرایش شد",
        )

        self.assertEqual(review.rating, 2)
        self.assertEqual(review.comment, "ویرایش شد")
        self.assertFalse(review.is_valid)

    def test_deactivate_review(self):
        """
        حذف منطقی نظر
        """

        review = create_review(
            product=self.product,
            user=self.user,
            rating=4,
            comment="نظر تست",
        )

        deactivate_review(
            review=review,
        )

        review.refresh_from_db()

        self.assertFalse(review.is_valid)

        self.assertEqual(
            review.comment,
            "[**توسط کاربر حذف شد**]\n\n",
        )

    def test_deactivate_review_does_not_delete_object(self):
        """
        حذف منطقی باعث حذف رکورد نمی‌شود.
        """

        review = create_review(
            product=self.product,
            user=self.user,
            rating=4,
            comment="نظر تست",
        )

        deactivate_review(
            review=review,
        )

        self.assertTrue(
            Review.objects.filter(
                pk=review.pk,
            ).exists()
        )