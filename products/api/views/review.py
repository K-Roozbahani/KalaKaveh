from rest_framework import status
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from products.api.serializers import (
    ReviewSerializer,
    ReviewWriteSerializer,
)
from products.selectors import (
    get_product_reviews,
    get_review_by_id,
    get_product_by_id,
)
from products.services.review import (
    create_review,
    update_review,
    deactivate_review,
)


class ReviewViewSet(
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    """
    API نظرات محصولات
    """

    lookup_field = "pk"

    def get_queryset(self):
        """
        لیست نظرات یک محصول
        """

        if "product_pk" in self.kwargs:
            return get_product_reviews(
                product_id=self.kwargs["product_pk"],
            )

        return get_product_reviews()

    def get_object(self):
        return get_review_by_id(
            review_id=self.kwargs["pk"],
        )

    def get_serializer_class(self):

        if self.action in (
            "create",
            "update",
            "partial_update",
        ):
            return ReviewWriteSerializer

        return ReviewSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        product = get_product_by_id(
            product_id=self.kwargs["product_pk"],
        )

        review = create_review(
            product=product,
            user=request.user,
            **serializer.validated_data,
        )

        return Response(
            ReviewSerializer(review).data,
            status=status.HTTP_201_CREATED,
        )

    def perform_update(self, serializer):

        update_review(
            review=self.get_object(),
            **serializer.validated_data,
        )

    def destroy(self, request, *args, **kwargs):
        review = self.get_object()

        deactivate_review(
            review=review,
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )