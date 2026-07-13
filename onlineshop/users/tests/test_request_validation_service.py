from django.test import TestCase

from users.exceptions import (
    IPAddressBlockedException,
    PhoneNumberBlockedException,
)
from users.services.request_validation import validate_request_source
from users.tests.factories import create_blacklist


class RequestValidationServiceTests(TestCase):
    """
    تست سرویس اعتبارسنجی منبع درخواست.
    """

    def test_validate_request_source_success(self):
        """
        شماره موبایل و IP مجاز باید بدون خطا عبور کنند.
        """
        validate_request_source(
            phone_number="09120000000",
            ip_address="192.168.1.10",
        )

    def test_validate_request_source_phone_blocked(self):
        """
        شماره موبایل بلاک شده باید Exception ایجاد کند.
        """
        create_blacklist(
            phone_number="09120000000",
        )

        with self.assertRaises(
            PhoneNumberBlockedException,
        ):
            validate_request_source(
                phone_number="09120000000",
                ip_address="192.168.1.10",
            )

    def test_validate_request_source_ip_blocked(self):
        """
        IP بلاک شده باید Exception ایجاد کند.
        """
        create_blacklist(
            ip_address="192.168.1.10",
        )

        with self.assertRaises(
            IPAddressBlockedException,
        ):
            validate_request_source(
                phone_number="09120000000",
                ip_address="192.168.1.10",
            )

    def test_validate_request_source_only_phone(self):
        """
        فقط شماره موبایل نیز باید معتبر باشد.
        """
        validate_request_source(
            phone_number="09120000000",
        )

    def test_validate_request_source_only_ip(self):
        """
        فقط IP نیز باید معتبر باشد.
        """
        validate_request_source(
            ip_address="192.168.1.10",
        )

    def test_validate_request_source_without_phone_and_ip(self):
        """
        در صورت نبود شماره موبایل و IP نباید خطایی ایجاد شود.
        """
        validate_request_source()