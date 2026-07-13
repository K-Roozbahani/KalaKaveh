from unittest.mock import ANY
from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.tests.factories import create_user


class AuthenticationApiTests(APITestCase):
    """
    تست API احراز هویت.
    """

    def setUp(self):
        self.request_otp_url = reverse(
            "authentication-request-otp",
        )

        self.verify_otp_url = reverse(
            "authentication-verify-otp",
        )

    @patch("users.api.views.request_otp")
    def test_request_otp_success(
        self,
        mock_request_otp,
    ):
        """
        درخواست موفق دریافت OTP.
        """
        response = self.client.post(
            self.request_otp_url,
            {
                "phone_number": "09120000000",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data,
            {
                "detail": "کد تأیید ارسال شد.",
            },
        )

        mock_request_otp.assert_called_once_with(
            phone_number=ANY,
            ip_address=ANY,
        )

    def test_request_otp_invalid_phone_number(self):
        """
        شماره موبایل نامعتبر باید خطای 400 برگرداند.
        """
        response = self.client.post(
            self.request_otp_url,
            {
                "phone_number": "123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    @patch("users.api.views.authenticate_by_otp")
    def test_verify_otp_success(
        self,
        mock_authenticate,
    ):
        """
        تأیید موفق OTP.
        """
        user = create_user()

        mock_authenticate.return_value = user

        response = self.client.post(
            self.verify_otp_url,
            {
                "phone_number": str(user.phone_number),
                "otp": "123456",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data,
            {
                "user_id": user.id,
            },
        )

        mock_authenticate.assert_called_once_with(
            phone_number=ANY,
            otp="123456",
            ip_address=ANY,
        )

    def test_verify_otp_invalid_phone_number(self):
        """
        شماره موبایل نامعتبر باید خطای 400 برگرداند.
        """
        response = self.client.post(
            self.verify_otp_url,
            {
                "phone_number": "123",
                "otp": "123456",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_verify_otp_invalid_otp(self):
        """
        کد تأیید نامعتبر باید خطای 400 برگرداند.
        """
        response = self.client.post(
            self.verify_otp_url,
            {
                "phone_number": "09120000000",
                "otp": "123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )