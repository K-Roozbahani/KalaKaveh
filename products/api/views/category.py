from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from products.api.serializers import CategorySerializer
from products.models import Category
from products.selectors import get_categories

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)


@extend_schema_view(
    list=extend_schema(
        summary="لیست دسته بندی",
        description="دریافت لیست دسته بندی",
    )
)
@extend_schema(
    tags=["categories"],
)
class CategoryViewSet(ListModelMixin, GenericViewSet):
    """
    API دسته‌بندی‌ها
    """

    serializer_class = CategorySerializer
    lookup_field = "slug"

    def get_queryset(self):
        return get_categories()