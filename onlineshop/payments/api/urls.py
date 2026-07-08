from django.urls import path
from rest_framework.routers import DefaultRouter

from payments.api.views import (
    PaymentViewSet,
    PaymentCallbackView,
)

router = DefaultRouter()

router.register(
    "",
    PaymentViewSet,
    basename="payments",
)

urlpatterns = [
    path(
        "callback/",
        PaymentCallbackView.as_view(),
        name="payment-callback",
    ),
]

urlpatterns += router.urls