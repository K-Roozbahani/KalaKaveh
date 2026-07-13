from django.test import TestCase

from users.selectors import (
    get_blacklisted_ip,
    get_blacklisted_phone,
    get_user_by_phone,
)
from users.tests.factories import (
    create_blacklist,
    create_user,
)


class UserSelectorTests(TestCase):
    """
    تست Selectorهای مربوط به کاربر.
    """

    def test_get_user_by_phone_returns_user(self):
        user = create_user()

        result = get_user_by_phone(user.phone_number)

        self.assertEqual(result, user)

    def test_get_user_by_phone_returns_none(self):
        result = get_user_by_phone("09129999999")

        self.assertIsNone(result)


class BlacklistSelectorTests(TestCase):
    """
    تست Selectorهای مربوط به بلک لیست.
    """

    def test_get_blacklisted_phone_returns_blacklist(self):
        blacklist = create_blacklist(
            phone_number="09121111111",
            is_active=True,
        )

        result = get_blacklisted_phone(
            blacklist.phone_number,
        )

        self.assertEqual(result, blacklist)

    def test_get_blacklisted_phone_returns_none(self):
        result = get_blacklisted_phone(
            "09129999999",
        )

        self.assertIsNone(result)

    def test_get_blacklisted_phone_returns_none_when_inactive(self):
        blacklist = create_blacklist(
            phone_number="09121111111",
            is_active=False,
        )

        result = get_blacklisted_phone(
            blacklist.phone_number,
        )

        self.assertIsNone(result)

    def test_get_blacklisted_ip_returns_blacklist(self):
        blacklist = create_blacklist(
            ip_address="192.168.1.10",
            is_active=True,
        )

        result = get_blacklisted_ip(
            "192.168.1.10",
        )

        self.assertEqual(result, blacklist)

    def test_get_blacklisted_ip_returns_none(self):
        result = get_blacklisted_ip(
            "8.8.8.8",
        )

        self.assertIsNone(result)

    def test_get_blacklisted_ip_returns_none_when_inactive(self):
        create_blacklist(
            ip_address="192.168.1.10",
            is_active=False,
        )

        result = get_blacklisted_ip(
            "192.168.1.10",
        )

        self.assertIsNone(result)