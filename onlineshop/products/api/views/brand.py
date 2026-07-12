from rest_framework.permissions import AllowAny
from rest_framework.viewsets import  GenericViewSet
from rest_framework.mixins import ListModelMixin

from products.api.serializers import BrandSerializer
from products.models import Brand
from products.selectors import get_brands

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)



@extend_schema_view(
    list=extend_schema(
        summary="لیست برند",
        description="دریافت لیست برند",
    )
)
@extend_schema(
    tags=["brands"],
)
class BrandViewSet(ListModelMixin, GenericViewSet):
    """
    API برندها
    """
    permission_classes = [AllowAny,]
    serializer_class = BrandSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return get_brands()