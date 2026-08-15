"""
سرویس تجمیع بررسی سلامت سیستم.
"""

from django.conf import settings

from health.services.base import HealthStatus
from health.services.celery import CeleryHealthService
from health.services.database import DatabaseHealthService
from health.services.redis import RedisHealthService


class HealthService:
    """
    سرویس تجمیع بررسی سلامت سیستم.
    """

    @staticmethod
    def check() -> dict:
        """
        وضعیت سلامت سرویس‌های سیستم را بررسی می‌کند.

        Returns:
            dict: نتایج بررسی سلامت سرویس‌ها.
        """
        services = {
            "database": DatabaseHealthService.check(),
            "redis": RedisHealthService.check(),
        }

        # در صورت فعال بودن، سلامت Celery نیز بررسی می‌شود.
        if getattr(settings, "HEALTH_CHECK_CELERY", False):
            services["celery"] = CeleryHealthService.check()

        overall_status = (
            HealthStatus.HEALTHY
            if all(service.is_healthy for service in services.values())
            else HealthStatus.UNHEALTHY
        )

        return {
            "status": overall_status.value,
            "services": {
                name: result.as_dict()
                for name, result in services.items()
            },
        }