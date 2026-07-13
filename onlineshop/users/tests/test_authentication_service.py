from unittest.mock import patch

from django.test import TestCase
from phonenumber_field.phonenumber import PhoneNumber

from users.services.authentication import (
    authenticate_by_otp,
    request_otp,
)


class AuthenticationServiceTests(TestCase):
    """
    تست سرویس احراز هویت.
    """

    def setUp(self):
        self.phone_number = PhoneNumber.from_string(
            phone_number="09120000000",
            region="IR",
        )

        self.ip_address = "192.168.1.10"

    @patch("users.services.authentication.send_otp")
    @patch("users.services.authentication.save_otp")
    @patch("users.services.authentication.generate_otp")
    @patch("users.services.authentication.check_rate_limit")
    @patch("users.services.authentication.validate_request_source")
    def test_request_otp(
        self,
        mock_validate_request_source,
        mock_check_rate_limit,
        mock_generate_otp,
        mock_save_otp,
        mock_send_otp,
    ):
        """
        باید OTP تولید، ذخیره و ارسال شود.
        """
        mock_generate_otp.return_value = "123456"

        request_otp(
            phone_number=self.phone_number,
            ip_address=self.ip_address,
        )

        mock_validate_request_source.assert_called_once_with(
            phone_number=self.phone_number,
            ip_address=self.ip_address,
        )

        mock_check_rate_limit.assert_called_once()

        mock_generate_otp.assert_called_once()

        mock_save_otp.assert_called_once_with(
            phone_number=str(self.phone_number),
            otp="123456",
        )

        mock_send_otp.assert_called_once_with(
            phone_number=str(self.phone_number),
            otp="123456",
        )

    @patch("users.services.authentication.get_or_create_user_by_phone")
    @patch("users.services.authentication.verify_otp")
    @patch("users.services.authentication.check_rate_limit")
    @patch("users.services.authentication.validate_request_source")
    def test_authenticate_by_otp(
        self,
        mock_validate_request_source,
        mock_check_rate_limit,
        mock_verify_otp,
        mock_get_or_create_user,
    ):
        """
        در صورت معتبر بودن OTP باید کاربر برگردانده شود.
        """
        user = object()

        mock_get_or_create_user.return_value = user

        result = authenticate_by_otp(
            phone_number=self.phone_number,
            otp="123456",
            ip_address=self.ip_address,
        )

        mock_validate_request_source.assert_called_once_with(
            phone_number=self.phone_number,
            ip_address=self.ip_address,
        )

        mock_check_rate_limit.assert_called_once()

        mock_verify_otp.assert_called_once_with(
            phone_number=str(self.phone_number),
            otp="123456",
        )

        mock_get_or_create_user.assert_called_once_with(
            phone_number=self.phone_number,
        )

        self.assertEqual(result, user)