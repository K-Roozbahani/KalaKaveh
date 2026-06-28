from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from products.models import Product
from products.selectors import (
    get_products_for_listing,
    get_product_detail_by_slug,
)
from products.api.filters import ProductFilter

from products.api.serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API محصولات فروشگاه
    """
    permission_classes = [AllowAny,]

    lookup_field = "slug"

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    filterset_class = ProductFilter

    search_fields = (
        "name",
        "description",
        "brand__name",
        "category__name",
    )

    ordering_fields = (
        "created_at",
        "name",
    )

    ordering = ("-created_at",)

    def get_queryset(self):
        """
        لیست محصولات از selector
        """

        if self.action == "retrieve":
            return Product.objects.all()

        return get_products_for_listing()


    def get_serializer_class(self):
        """
        انتخاب serializer مناسب
        """

        if self.action == "retrieve":
            return ProductDetailSerializer

        return ProductListSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        جزئیات محصول
        """

        product = get_product_detail_by_slug(
            slug=kwargs["slug"],
        )

        serializer = self.get_serializer(product)

        return Response(serializer.data)

