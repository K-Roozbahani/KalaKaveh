from rest_framework.routers import (
    DefaultRouter,
)

from shipping.api.views import (
    ShippingMethodViewSet,
    ShipmentViewSet,
)

router = DefaultRouter()

router.register(
    "shipping-methods",
    ShippingMethodViewSet,
    basename="shipping-methods",
)

router.register(
    "shipments",
    ShipmentViewSet,
    basename="shipments",
)

urlpatterns = router.urls