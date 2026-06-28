from rest_framework.viewsets import  GenericViewSet
from rest_framework.mixins import ListModelMixin

from products.api.serializers import BrandSerializer
from products.models import Brand
from products.selectors import get_brands


class BrandViewSet(ListModelMixin, GenericViewSet):
    """
    API برندها
    """

    serializer_class = BrandSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return get_brands()