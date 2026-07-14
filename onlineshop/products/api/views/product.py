from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from products.api.pagination import ProductPagination
from products.facet_selectors import ProductFacetSelector
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

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

from products.services.product import prepare_retrieve_product_by_slug


@extend_schema_view(
    list=extend_schema(
        summary="لیست محصولات",
        description="دریافت لیست محصولات فعال فروشگاه",
        responses=ProductListSerializer
    ),
    retrieve=extend_schema(
        summary="جزئیات محصول",
        description="دریافت اطلاعات کامل یک محصول بر اساس اسلاگ",
        responses=ProductDetailSerializer
    ),
)
@extend_schema(
    tags=["Products"],
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
        "default_price",
    )

    ordering = ("-created_at",)

    pagination_class = ProductPagination

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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            self.get_queryset()
        )

        # استخراج اطلاعات فیلترها قبل از Pagination
        facets = ProductFacetSelector.get_facets(
            queryset=queryset,
        )

        page = self.paginate_queryset(
            queryset,
        )

        if page is not None:
            serializer = self.get_serializer(
                page,
                many=True,
            )

            response = self.get_paginated_response(
                serializer.data,
            )

            response.data["facets"] = facets

            return response

        serializer = self.get_serializer(
            queryset,
            many=True,
        )

        return Response(
            {
                "facets": facets,
                "results": serializer.data,
            }
        )

    def retrieve(self, request, *args, **kwargs):
        """
        جزئیات محصول
        """

        product = prepare_retrieve_product_by_slug(
            slug=kwargs["slug"],
        )

        serializer = self.get_serializer(product)

        return Response(serializer.data)

