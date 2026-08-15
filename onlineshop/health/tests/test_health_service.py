"""
تست‌های سرویس تجمیع بررسی سلامت سیستم.
"""

from unittest.mock import patch

from django.test import SimpleTestCase, override_settings

from health.services.base import HealthResult, HealthStatus
from health.services.health import HealthService


class HealthServiceTestCase(SimpleTestCase):
    """
    تست‌های سرویس تجمیع بررسی سلامت سیستم.
    """

    @patch("health.services.health.RedisHealthService.check")
    @patch("health.services.health.DatabaseHealthService.check")
    @override_settings(HEALTH_CHECK_CELERY=False)
    def test_check_returns_healthy_when_all_services_are_healthy(
        self,
        mock_database_check,
        mock_redis_check,
    ):
        """
        در صورت سالم بودن تمام سرویس‌ها باید وضعیت کلی HEALTHY برگردد.
        """
        mock_database_check.return_value = HealthResult(
            status=HealthStatus.HEALTHY,
            latency_ms=10,
            message="Database is available.",
        )

        mock_redis_check.return_value = HealthResult(
            status=HealthStatus.HEALTHY,
            latency_ms=5,
            message="Redis is available.",
        )

        result = HealthService.check()

        self.assertEqual(result["status"], HealthStatus.HEALTHY.value)
        self.assertIn("database", result["services"])
        self.assertIn("redis", result["services"])
        self.assertNotIn("celery", result["services"])

    @patch("health.services.health.RedisHealthService.check")
    @patch("health.services.health.DatabaseHealthService.check")
    @override_settings(HEALTH_CHECK_CELERY=False)
    def test_check_returns_unhealthy_when_any_service_is_unhealthy(
        self,
        mock_database_check,
        mock_redis_check,
    ):
        """
        در صورت ناسالم بودن یکی از سرویس‌ها باید وضعیت کلی UNHEALTHY برگردد.
        """
        mock_database_check.return_value = HealthResult(
            status=HealthStatus.UNHEALTHY,
            latency_ms=None,
            message="Database is unavailable.",
        )

        mock_redis_check.return_value = HealthResult(
            status=HealthStatus.HEALTHY,
            latency_ms=5,
            message="Redis is available.",
        )

        result = HealthService.check()

        self.assertEqual(result["status"], HealthStatus.UNHEALTHY.value)

    @patch("health.services.health.CeleryHealthService.check")
    @patch("health.services.health.RedisHealthService.check")
    @patch("health.services.health.DatabaseHealthService.check")
    @override_settings(HEALTH_CHECK_CELERY=True)
    def test_check_includes_celery_when_enabled(
        self,
        mock_database_check,
        mock_redis_check,
        mock_celery_check,
    ):
        """
        در صورت فعال بودن HEALTH_CHECK_CELERY باید Celery نیز بررسی شود.
        """
        mock_database_check.return_value = HealthResult(
            status=HealthStatus.HEALTHY,
            latency_ms=10,
            message="Database is available.",
        )

        mock_redis_check.return_value = HealthResult(
            status=HealthStatus.HEALTHY,
            latency_ms=5,
            message="Redis is available.",
        )

        mock_celery_check.return_value = HealthResult(
            status=HealthStatus.HEALTHY,
            latency_ms=3,
            message="Celery workers are available.",
        )

        result = HealthService.check()

        mock_celery_check.assert_called_once()

        self.assertIn("celery", result["services"])
        self.assertEqual(result["status"], HealthStatus.HEALTHY.value)

    @patch("health.services.health.CeleryHealthService.check")
    @patch("health.services.health.RedisHealthService.check")
    @patch("health.services.health.DatabaseHealthService.check")
    @override_settings(HEALTH_CHECK_CELERY=False)
    def test_check_does_not_call_celery_when_disabled(
        self,
        mock_database_check,
        mock_redis_check,
        mock_celery_check,
    ):
        """
        در صورت غیرفعال بودن HEALTH_CHECK_CELERY نباید Celery بررسی شود.
        """
        mock_database_check.return_value = HealthResult(
            status=HealthStatus.HEALTHY,
            latency_ms=10,
            message="Database is available.",
        )

        mock_redis_check.return_value = HealthResult(
            status=HealthStatus.HEALTHY,
            latency_ms=5,
            message="Redis is available.",
        )

        result = HealthService.check()

        mock_celery_check.assert_not_called()

        self.assertNotIn("celery", result["services"])
        self.assertEqual(result["status"], HealthStatus.HEALTHY.value)