"""
سرویس بررسی سلامت پایگاه داده.
"""

import logging
from time import perf_counter

from django.db import connections
from django.db.utils import DatabaseError

from health.services.base import HealthResult, HealthStatus

logger = logging.getLogger(__name__)


class DatabaseHealthService:
    """
    سرویس بررسی سلامت پایگاه داده.
    """

    @staticmethod
    def check() -> HealthResult:
        """
        اتصال به پایگاه داده را بررسی می‌کند.

        Returns:
            HealthResult: نتیجه بررسی سلامت پایگاه داده.
        """
        start_time = perf_counter()

        try:
            with connections["default"].cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()

            latency = round((perf_counter() - start_time) * 1000, 2)

            return HealthResult(
                status=HealthStatus.HEALTHY,
                latency_ms=latency,
                message="Database is available.",
            )

        except DatabaseError:
            logger.exception("Database health check failed.")

        except Exception:
            logger.exception(
                "Unexpected error occurred during database health check."
            )

        return HealthResult(
            status=HealthStatus.UNHEALTHY,
            latency_ms=None,
            message="Database is unavailable.",
        )