"""
تست‌های سرویس بررسی سلامت Redis.
"""

from unittest.mock import patch

from django.test import SimpleTestCase

from health.services.base import HealthStatus
from health.services.redis import RedisHealthService


class RedisHealthServiceTestCase(SimpleTestCase):
    """
    تست‌های سرویس بررسی سلامت Redis.
    """

    @patch("health.services.redis.cache")
    def test_check_returns_healthy_when_redis_is_available(
        self,
        mock_cache,
    ):
        """
        در صورت موفق بودن عملیات خواندن و نوشتن باید وضعیت HEALTHY برگردد.
        """
        mock_cache.get.return_value = "ok"

        result = RedisHealthService.check()

        mock_cache.set.assert_called_once_with(
            "__health_check__",
            "ok",
            timeout=5,
        )
        mock_cache.get.assert_called_once_with("__health_check__")

        self.assertEqual(result.status, HealthStatus.HEALTHY)
        self.assertTrue(result.is_healthy)
        self.assertIsNotNone(result.latency_ms)
        self.assertEqual(result.message, "Redis is available.")

    @patch("health.services.redis.cache")
    def test_check_returns_unhealthy_when_read_write_validation_fails(
        self,
        mock_cache,
    ):
        """
        در صورت نامعتبر بودن مقدار خوانده شده باید وضعیت UNHEALTHY برگردد.
        """
        mock_cache.get.return_value = "invalid"

        result = RedisHealthService.check()

        self.assertEqual(result.status, HealthStatus.UNHEALTHY)
        self.assertFalse(result.is_healthy)
        self.assertIsNone(result.latency_ms)
        self.assertEqual(result.message, "Redis is unavailable.")

    @patch("health.services.redis.cache")
    def test_check_returns_unhealthy_when_exception_occurs(
        self,
        mock_cache,
    ):
        """
        در صورت وقوع خطا باید وضعیت UNHEALTHY برگردد.
        """
        mock_cache.set.side_effect = Exception

        result = RedisHealthService.check()

        self.assertEqual(result.status, HealthStatus.UNHEALTHY)
        self.assertFalse(result.is_healthy)
        self.assertIsNone(result.latency_ms)
        self.assertEqual(result.message, "Redis is unavailable.")