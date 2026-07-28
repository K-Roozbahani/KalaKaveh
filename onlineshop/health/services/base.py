"""
کلاس‌ها و ساختارهای پایه برای سیستم Health Check پروژه.
"""

from dataclasses import dataclass
from enum import StrEnum


class HealthStatus(StrEnum):
    """وضعیت سلامت سرویس."""

    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


@dataclass(slots=True, frozen=True)
class HealthResult:
    """
    نتیجه بررسی سلامت یک سرویس.
    """

    status: HealthStatus
    latency_ms: float | None = None
    message: str = ""

    @property
    def is_healthy(self) -> bool:
        """
        آیا سرویس سالم است؟
        """
        return self.status == HealthStatus.HEALTHY

    def as_dict(self) -> dict:
        """
        تبدیل نتیجه به دیکشنری جهت استفاده در Serializer یا Response.
        """
        return {
            "status": self.status.value,
            "latency_ms": self.latency_ms,
            "message": self.message,
        }