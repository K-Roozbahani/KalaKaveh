"""
URLهای مربوط به Health Check.
"""

from django.urls import path

from health.api.views import HealthCheckAPIView

app_name = "health"

urlpatterns = [
    path(
        "",
        HealthCheckAPIView.as_view(),
        name="check",
    ),
]