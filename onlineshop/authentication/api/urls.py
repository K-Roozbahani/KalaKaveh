from rest_framework.routers import DefaultRouter

from authentication.api.views.auth import AuthenticationViewSet
from authentication.api.views.csrf import CSRFTokenView

from django.urls import path

router = DefaultRouter()


urlpatterns = [
    path(
        "csrf/",
        CSRFTokenView.as_view(),
        name="csrf-token",
    ),
]

router.register("", AuthenticationViewSet, basename="authentication")

urlpatterns += router.urls