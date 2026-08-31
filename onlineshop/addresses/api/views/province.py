from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated

from addresses.api.serializers import (
    ProvinceWithCitiesSerializer,
)
from addresses.selectors import get_provinces_with_cities

from utils.api.views import BaseGenericViewSet


class ProvinceViewSet(
    ListModelMixin,
    BaseGenericViewSet,
):
    """
    API دریافت لیست استان‌ها به همراه شهرهای هر استان.
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = ProvinceWithCitiesSerializer

    def get_queryset(self):
        """
        دریافت استان‌ها به همراه شهرهای زیرمجموعه.
        """

        return get_provinces_with_cities()