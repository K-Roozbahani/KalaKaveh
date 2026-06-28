from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from products.api.serializers import CategorySerializer
from products.models import Category
from products.selectors import get_categories


class CategoryViewSet(ListModelMixin, GenericViewSet):
    """
    API دسته‌بندی‌ها
    """

    serializer_class = CategorySerializer
    lookup_field = "slug"

    def get_queryset(self):
        return get_categories()