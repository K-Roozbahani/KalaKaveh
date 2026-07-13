from django.test import TestCase

from users.exceptions import (
    IPAddressBlockedException,
    PhoneNumberBlockedException,
)
from users.tests.factories import create_blacklist
from users.validators import (
    validate_ip_blacklist,
    validate_phone_blacklist,
)


class PhoneBlacklistValidatorTests(TestCase):
    """
    تست اعتبارسنجی بلک لیست شماره موبایل.
    """

    def test_validate_phone_blacklist_success(self):
        """
        شماره موبایل مجاز باید بدون خطا عبور کند.
        """
        try:
            validate_phone_blacklist("09120000000")
        except Exception:
            self.fail("Phone number should not be blocked.")

    def test_validate_phone_blacklist_blocked(self):
        """
        شماره موبایل بلاک شده باید Exception ایجاد کند.
        """
        create_blacklist(
            phone_number="09120000000",
            is_active=True,
        )

        with self.assertRaises(PhoneNumberBlockedException):
            validate_phone_blacklist("09120000000")


class IPBlacklistValidatorTests(TestCase):
    """
    تست اعتبارسنجی بلک لیست IP.
    """

    def test_validate_ip_blacklist_success(self):
        """
        IP مجاز باید بدون خطا عبور کند.
        """
        try:
            validate_ip_blacklist("192.168.1.1")
        except Exception:
            self.fail("IP address should not be blocked.")

    def test_validate_ip_blacklist_blocked(self):
        """
        IP بلاک شده باید Exception ایجاد کند.
        """
        create_blacklist(
            ip_address="192.168.1.1",
            is_active=True,
        )

        with self.assertRaises(IPAddressBlockedException):
            validate_ip_blacklist("192.168.1.1")