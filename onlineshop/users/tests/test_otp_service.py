from django.core.cache import cache
from django.test import TestCase

from users.constants import (
    OTP_LENGTH,
    OTP_TTL,
    REDIS_KEY_OTP,
)
from users.exceptions import (
    InvalidOTPException,
    OTPExpiredException,
)
from users.services.otp import (
    delete_otp,
    generate_otp,
    get_otp,
    save_otp,
    verify_otp,
)


class OTPServiceTests(TestCase):
    """
    تست سرویس‌های OTP.
    """

    PHONE_NUMBER = "09120000000"

    def setUp(self):
        cache.clear()

    def test_generate_otp_returns_string(self):
        """
        OTP باید از نوع رشته باشد.
        """
        otp = generate_otp()

        self.assertIsInstance(otp, str)

    def test_generate_otp_length(self):
        """
        طول OTP باید مطابق تنظیمات باشد.
        """
        otp = generate_otp()

        self.assertEqual(
            len(otp),
            OTP_LENGTH,
        )

    def test_generate_otp_is_numeric(self):
        """
        OTP باید فقط شامل اعداد باشد.
        """
        otp = generate_otp()

        self.assertTrue(
            otp.isdigit(),
        )

    def test_save_otp(self):
        """
        OTP باید در Redis ذخیره شود.
        """
        save_otp(
            phone_number=self.PHONE_NUMBER,
            otp="123456",
        )

        redis_key = REDIS_KEY_OTP.format(
            phone=self.PHONE_NUMBER,
        )

        self.assertEqual(
            cache.get(redis_key),
            "123456",
        )

    def test_get_otp(self):
        """
        OTP ذخیره شده باید قابل دریافت باشد.
        """
        save_otp(
            phone_number=self.PHONE_NUMBER,
            otp="123456",
        )

        otp = get_otp(
            phone_number=self.PHONE_NUMBER,
        )

        self.assertEqual(
            otp,
            "123456",
        )

    def test_delete_otp(self):
        """
        حذف OTP باید کلید Redis را حذف کند.
        """
        save_otp(
            phone_number=self.PHONE_NUMBER,
            otp="123456",
        )

        delete_otp(
            phone_number=self.PHONE_NUMBER,
        )

        otp = get_otp(
            phone_number=self.PHONE_NUMBER,
        )

        self.assertIsNone(otp)

    def test_verify_otp_success(self):
        """
        OTP صحیح باید تأیید و حذف شود.
        """
        save_otp(
            phone_number=self.PHONE_NUMBER,
            otp="123456",
        )

        verify_otp(
            phone_number=self.PHONE_NUMBER,
            otp="123456",
        )

        self.assertIsNone(
            get_otp(
                phone_number=self.PHONE_NUMBER,
            )
        )

    def test_verify_otp_invalid(self):
        """
        OTP اشتباه باید InvalidOTPException ایجاد کند.
        """
        save_otp(
            phone_number=self.PHONE_NUMBER,
            otp="123456",
        )

        with self.assertRaises(
            InvalidOTPException,
        ):
            verify_otp(
                phone_number=self.PHONE_NUMBER,
                otp="654321",
            )

    def test_verify_otp_expired(self):
        """
        در صورت نبود OTP باید OTPExpiredException ایجاد شود.
        """
        with self.assertRaises(
            OTPExpiredException,
        ):
            verify_otp(
                phone_number=self.PHONE_NUMBER,
                otp="123456",
            )

    def test_save_otp_timeout(self):
        """
        OTP باید با زمان انقضای صحیح ذخیره شود.
        """
        save_otp(
            phone_number=self.PHONE_NUMBER,
            otp="123456",
        )

        redis_key = REDIS_KEY_OTP.format(
            phone=self.PHONE_NUMBER,
        )

        ttl = cache.ttl(redis_key)

        self.assertGreater(
            ttl,
            0,
        )

        self.assertLessEqual(
            ttl,
            OTP_TTL,
        )