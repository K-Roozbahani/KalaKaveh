from rest_framework import viewsets

from rest_framework.permissions import AllowAny

from discounts.api.schemas.discount import discount_schema
from discounts.selectors import get_active_discounts

from discounts.api.serializers.discount import (
    DiscountListSerializer,
    DiscountDetailSerializer,
)


@discount_schema
class DiscountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API تخفیف‌های فعال.
    """

    lookup_field = "slug"


    permission_classes = [AllowAny]
    def get_queryset(self):
        return get_active_discounts()

    def get_serializer_class(self):
        if self.action == "list":
            return DiscountListSerializer

        return DiscountDetailSerializer