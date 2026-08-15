"""
View مربوط به بررسی سلامت سیستم.
"""

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from health.services.base import HealthStatus
from health.services.health import HealthService


class HealthCheckAPIView(APIView):
    """
    نمایش وضعیت سلامت سیستم.
    """

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request):
        """
        وضعیت سلامت سیستم را برمی‌گرداند.
        """
        result = HealthService.check()

        http_status = (
            status.HTTP_200_OK
            if result["status"] == HealthStatus.HEALTHY.value
            else status.HTTP_503_SERVICE_UNAVAILABLE
        )

        return Response(
            data=result,
            status=http_status,
        )