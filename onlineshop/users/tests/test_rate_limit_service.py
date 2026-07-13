from django.core.cache import cache
from django.test import TestCase

from users.constants import (
    RATE_LIMITS,
    REDIS_KEY_RATE_LIMIT,
)
from users.exceptions import RateLimitExceededException
from users.services.rate_limit import check_rate_limit


class RateLimitServiceTests(TestCase):
    """
    تست سرویس Rate Limit.
    """

    def setUp(self):
        cache.clear()

    def test_check_rate_limit_first_request(self):
        """
        اولین درخواست باید بدون خطا ثبت شود.
        """
        check_rate_limit(
            action="otp_request",
            identifier="09120000000",
        )

    def test_check_rate_limit_sets_counter(self):
        check_rate_limit(
            action="otp_request",
            identifier="09120000000",
        )

        config = RATE_LIMITS["otp_request"][0]

        redis_key = REDIS_KEY_RATE_LIMIT.format(
            action="otp_request",
            identifier="09120000000",
            period=config["name"],
        )

        self.assertEqual(
            cache.get(redis_key),
            1,
        )

    def test_check_rate_limit_reaches_limit(self):
        """
        رسیدن به سقف مجاز باید باعث Exception شود.
        """
        config = RATE_LIMITS["otp_request"][0]

        redis_key = REDIS_KEY_RATE_LIMIT.format(
            action="otp_request",
            identifier="09120000000",
            period=config["name"],
        )

        cache.set(
            redis_key,
            config["limit"],
            timeout=config["window"],
        )

        with self.assertRaises(
            RateLimitExceededException,
        ):
            check_rate_limit(
                action="otp_request",
                identifier="09120000000",
            )

    def test_check_rate_limit_unknown_action(self):
        """
        اگر Action تعریف نشده باشد نباید خطایی ایجاد شود.
        """
        check_rate_limit(
            action="unknown_action",
            identifier="09120000000",
        )

    def test_check_rate_limit_creates_all_windows(self):
        """
        باید برای تمام Windowهای تعریف شده شمارنده ایجاد شود.
        """
        check_rate_limit(
            action="otp_request",
            identifier="09120000000",
        )

        for config in RATE_LIMITS["otp_request"]:
            redis_key = REDIS_KEY_RATE_LIMIT.format(
                action="otp_request",
                identifier="09120000000",
                period=config["name"],
            )

            self.assertEqual(
                cache.get(redis_key),
                1,
            )