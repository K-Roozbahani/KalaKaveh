from rest_framework import (
    mixins,
)

from rest_framework.permissions import (
    IsAuthenticated,
)

from shipping.serializers import (
    ShippingMethodSerializer,
    ShipmentListSerializer,
    ShipmentDetailSerializer,
)

from shipping.selectors import (
    get_active_shipping_methods,
    get_user_shipments,
)

from shipping.api.schemas import (
    schema_shipment,
    schema_shipping_method,
)

from utils.api.views import BaseGenericViewSet


@schema_shipping_method
class ShippingMethodViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    BaseGenericViewSet,
):
    """
    نمایش روش‌های ارسال فعال
    """

    serializer_class = (
        ShippingMethodSerializer
    )

    permission_classes = (
        IsAuthenticated,
    )

    pagination_class = None

    def get_queryset(self):
        return get_active_shipping_methods()


@schema_shipment
class ShipmentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    BaseGenericViewSet,
):
    """
    نمایش مرسوله‌های کاربر
    """

    permission_classes = (
        IsAuthenticated,
    )

    def get_queryset(self):
        return get_user_shipments(
            user=self.request.user,
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ShipmentDetailSerializer

        return ShipmentListSerializer