from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from products.models import Product
from products.selectors import (
    get_products_for_listing,
    get_product_detail_by_slug,
)

from products.api.serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API محصولات فروشگاه

    فقط خواندنی (Read Only)
    """

    lookup_field = "slug"

    def get_queryset(self):
        """
        انتخاب queryset بر اساس action
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
        دریافت جزئیات محصول بر اساس slug
        """

        product = get_product_detail_by_slug(
            slug=kwargs["slug"],
        )

        serializer = self.get_serializer(product)

        return Response(serializer.data)

