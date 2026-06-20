from rest_framework import (
    mixins,
    viewsets,
)

from rest_framework.permissions import (
    IsAuthenticated,
)

from shipping.models import (
    ShippingMethod,
    Shipment,
)

from shipping.serializers import (
    ShippingMethodSerializer,
    ShipmentListSerializer,
    ShipmentDetailSerializer,
)

from shipping.selectors import (
    get_active_shipping_methods,
    get_user_shipments,
    get_user_shipment_by_id,
)


class ShippingMethodViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
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


class ShipmentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
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