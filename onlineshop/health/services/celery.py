"""
سرویس بررسی سلامت Celery.
"""

import logging
from time import perf_counter

from celery import current_app

from health.services.base import HealthResult, HealthStatus

logger = logging.getLogger(__name__)


class CeleryHealthService:
    """
    سرویس بررسی سلامت Workerهای Celery.
    """

    @staticmethod
    def check() -> HealthResult:
        """
        وضعیت Workerهای Celery را بررسی می‌کند.

        Returns:
            HealthResult: نتیجه بررسی سلامت Celery.
        """
        start_time = perf_counter()

        try:
            inspector = current_app.control.inspect(timeout=2.0)
            workers = inspector.ping()

            if not workers:
                logger.warning("No active Celery workers found.")

                return HealthResult(
                    status=HealthStatus.UNHEALTHY,
                    latency_ms=None,
                    message="No active Celery workers.",
                )

            latency = round((perf_counter() - start_time) * 1000, 2)

            return HealthResult(
                status=HealthStatus.HEALTHY,
                latency_ms=latency,
                message="Celery workers are available.",
            )

        except Exception:
            logger.exception("Celery health check failed.")

        return HealthResult(
            status=HealthStatus.UNHEALTHY,
            latency_ms=None,
            message="Celery is unavailable.",
        )