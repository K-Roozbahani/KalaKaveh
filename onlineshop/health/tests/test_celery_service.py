"""
تست‌های سرویس بررسی سلامت Celery.
"""

from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase

from health.services.base import HealthStatus
from health.services.celery import CeleryHealthService


class CeleryHealthServiceTestCase(SimpleTestCase):
    """
    تست‌های سرویس بررسی سلامت Celery.
    """

    @patch("health.services.celery.current_app")
    def test_check_returns_healthy_when_worker_is_available(
        self,
        mock_current_app,
    ):
        """
        در صورت فعال بودن Worker باید وضعیت HEALTHY برگردد.
        """
        mock_inspector = MagicMock()
        mock_inspector.ping.return_value = {
            "celery@worker": {"ok": "pong"},
        }

        mock_current_app.control.inspect.return_value = mock_inspector

        result = CeleryHealthService.check()

        mock_current_app.control.inspect.assert_called_once_with(
            timeout=2.0,
        )
        mock_inspector.ping.assert_called_once()

        self.assertEqual(result.status, HealthStatus.HEALTHY)
        self.assertTrue(result.is_healthy)
        self.assertIsNotNone(result.latency_ms)
        self.assertEqual(
            result.message,
            "Celery workers are available.",
        )

    @patch("health.services.celery.current_app")
    def test_check_returns_unhealthy_when_no_worker_is_available(
        self,
        mock_current_app,
    ):
        """
        در صورت نبود Worker باید وضعیت UNHEALTHY برگردد.
        """
        mock_inspector = MagicMock()
        mock_inspector.ping.return_value = {}

        mock_current_app.control.inspect.return_value = mock_inspector

        result = CeleryHealthService.check()

        self.assertEqual(result.status, HealthStatus.UNHEALTHY)
        self.assertFalse(result.is_healthy)
        self.assertIsNone(result.latency_ms)
        self.assertEqual(
            result.message,
            "No active Celery workers.",
        )

    @patch("health.services.celery.current_app")
    def test_check_returns_unhealthy_when_exception_occurs(
        self,
        mock_current_app,
    ):
        """
        در صورت وقوع خطا باید وضعیت UNHEALTHY برگردد.
        """
        mock_current_app.control.inspect.side_effect = Exception

        result = CeleryHealthService.check()

        self.assertEqual(result.status, HealthStatus.UNHEALTHY)
        self.assertFalse(result.is_healthy)
        self.assertIsNone(result.latency_ms)
        self.assertEqual(
            result.message,
            "Celery is unavailable.",
        )