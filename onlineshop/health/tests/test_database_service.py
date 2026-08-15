"""
تست‌های سرویس بررسی سلامت پایگاه داده.
"""

from unittest.mock import MagicMock, patch

from django.db.utils import DatabaseError
from django.test import SimpleTestCase

from health.services.base import HealthStatus
from health.services.database import DatabaseHealthService


class DatabaseHealthServiceTestCase(SimpleTestCase):
    """
    تست‌های سرویس بررسی سلامت پایگاه داده.
    """

    @patch("health.services.database.connections")
    def test_check_returns_healthy_when_database_is_available(
        self,
        mock_connections,
    ):
        """
        در صورت برقراری اتصال به پایگاه داده باید وضعیت HEALTHY برگردد.
        """
        mock_cursor = MagicMock()

        mock_connections.__getitem__.return_value.cursor.return_value.__enter__.return_value = (
            mock_cursor
        )

        result = DatabaseHealthService.check()

        mock_cursor.execute.assert_called_once_with("SELECT 1")
        mock_cursor.fetchone.assert_called_once()

        self.assertEqual(result.status, HealthStatus.HEALTHY)
        self.assertTrue(result.is_healthy)
        self.assertIsNotNone(result.latency_ms)
        self.assertEqual(result.message, "Database is available.")

    @patch("health.services.database.connections")
    def test_check_returns_unhealthy_when_database_error_occurs(
        self,
        mock_connections,
    ):
        """
        در صورت وقوع DatabaseError باید وضعیت UNHEALTHY برگردد.
        """
        mock_connections.__getitem__.return_value.cursor.side_effect = DatabaseError

        result = DatabaseHealthService.check()

        self.assertEqual(result.status, HealthStatus.UNHEALTHY)
        self.assertFalse(result.is_healthy)
        self.assertIsNone(result.latency_ms)
        self.assertEqual(result.message, "Database is unavailable.")

    @patch("health.services.database.connections")
    def test_check_returns_unhealthy_when_unexpected_exception_occurs(
        self,
        mock_connections,
    ):
        """
        در صورت وقوع خطای غیرمنتظره باید وضعیت UNHEALTHY برگردد.
        """
        mock_connections.__getitem__.return_value.cursor.side_effect = RuntimeError

        result = DatabaseHealthService.check()

        self.assertEqual(result.status, HealthStatus.UNHEALTHY)
        self.assertFalse(result.is_healthy)
        self.assertIsNone(result.latency_ms)
        self.assertEqual(result.message, "Database is unavailable.")