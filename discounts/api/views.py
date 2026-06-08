from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from discounts.api.serializers.coupon import CouponSerializer
from discounts.api.serializers.usage import CouponUsageSerializer

from discounts.models import (
    Discount,
    DiscountTarget,
    Coupon,
    CouponUsage,
)

from discounts.api.serializers.discount import (
    DiscountListSerializer,
    DiscountDetailSerializer,
    DiscountCreateUpdateSerializer,
)



class DiscountViewSet(ModelViewSet):

    queryset = (
        Discount.objects
        .prefetch_related("targets")
        .order_by("-priority")
    )

    def get_serializer_class(self):

        if self.action == "list":
            return DiscountListSerializer

        if self.action in (
            "create",
            "update",
            "partial_update"
        ):
            return DiscountCreateUpdateSerializer

        return DiscountDetailSerializer


class CouponViewSet(ModelViewSet):

    queryset = Coupon.objects.select_related(
        "discount"
    )

    serializer_class = CouponSerializer


class CouponUsageViewSet(
    ReadOnlyModelViewSet
):

    queryset = (
        CouponUsage.objects
        .select_related(
            "coupon",
            "user",
            "order"
        )
    )

    serializer_class = (
        CouponUsageSerializer
    )