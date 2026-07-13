from django.test import TestCase

from users.models import User
from users.services.user import get_or_create_user_by_phone
from users.tests.factories import create_user


class UserServiceTests(TestCase):
    """
    تست سرویس‌های مربوط به کاربران.
    """

    def test_get_or_create_user_by_phone_returns_existing_user(self):
        """
        در صورت وجود کاربر، همان کاربر باید برگردانده شود.
        """
        user = create_user(
            phone_number="09120000000",
        )

        result = get_or_create_user_by_phone(
            phone_number=user.phone_number,
        )

        self.assertEqual(result, user)

        self.assertEqual(User.objects.count(), 1)

    def test_get_or_create_user_by_phone_creates_new_user(self):
        """
        در صورت نبود کاربر، باید کاربر جدید ایجاد شود.
        """
        result = get_or_create_user_by_phone(
            phone_number="09121111111",
        )

        self.assertIsInstance(result, User)

        self.assertTrue(
            User.objects.filter(
                phone_number=result.phone_number,
            ).exists()
        )

        self.assertEqual(User.objects.count(), 1)