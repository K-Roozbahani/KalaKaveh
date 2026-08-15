"""
سرویس بررسی سلامت Redis.
"""

import logging
from time import perf_counter

from django.core.cache import cache

from health.services.base import HealthResult, HealthStatus

logger = logging.getLogger(__name__)


class RedisHealthService:
    """
    سرویس بررسی سلامت Redis.
    """

    @staticmethod
    def check() -> HealthResult:
        """
        اتصال به Redis را بررسی می‌کند.

        Returns:
            HealthResult: نتیجه بررسی سلامت Redis.
        """
        start_time = perf_counter()

        try:
            cache.set("__health_check__", "ok", timeout=5)
            value = cache.get("__health_check__")

            if value != "ok":
                raise RuntimeError("Redis read/write validation failed.")

            latency = round((perf_counter() - start_time) * 1000, 2)

            return HealthResult(
                status=HealthStatus.HEALTHY,
                latency_ms=latency,
                message="Redis is available.",
            )

        except Exception:
            logger.exception("Redis health check failed.")

        return HealthResult(
            status=HealthStatus.UNHEALTHY,
            latency_ms=None,
            message="Redis is unavailable.",
        )