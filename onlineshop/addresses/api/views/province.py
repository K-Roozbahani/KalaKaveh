from rest_framework import mixins, viewsets

from addresses.api.serializers import (
    ProvinceWithCitiesSerializer,
)
from addresses.selectors import get_provinces_with_cities


class ProvinceViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    API دریافت لیست استان‌ها به همراه شهرهای هر استان.
    """

    serializer_class = ProvinceWithCitiesSerializer

    def get_queryset(self):
        """
        دریافت استان‌ها به همراه شهرهای زیرمجموعه.
        """

        return get_provinces_with_cities()