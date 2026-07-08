from rest_framework import status
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin, DestroyModelMixin,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from utils.permissions import IsOwnerOrAdmin

from products.api.serializers.review import (
    ReviewSerializer,
    ReviewWriteSerializer,
)
from products.selectors import (
    get_product_by_id,
    get_product_reviews,
    get_review_by_id,
)
from products.services.review import (
    create_review,
    update_review,
    deactivate_review,
)

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)


@extend_schema_view(
    list=extend_schema(
        summary="لیست نظرات",
        description="دریافت لیست نظرات معتبر",
        responses=ReviewSerializer,

    ),
    create=extend_schema(
        summary="ثبت نظر",
        description="ثبت نظر جدید کاربر یا بروزرسانی نظر ثبت شده کاربر",
        responses=ReviewWriteSerializer,
    ),
    update=extend_schema(
        summary="بروز رسانی نظر",
        description="بروزرسانی نظر ثبت شده کاربر",
        responses=ReviewWriteSerializer,
    ),
    destroy=extend_schema(
        summary="حذف نظر کاربر",
        description="حذف نظر کاربر نظر ثبت شده",
    ),

)
@extend_schema(
    tags=["review"],
)
class ReviewViewSet(
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    """
    مدیریت نظرات محصولات
    """

    def get_permissions(self):
        """
        تعیین Permission بر اساس Action
        """

        if self.action in (
            "list",
            "retrieve",
        ):
            permission_classes = [
                AllowAny,
            ]

        elif self.action == "create":
            permission_classes = [
                IsAuthenticated,
            ]

        else:
            permission_classes = [
                IsOwnerOrAdmin,
            ]

        return [
            permission()
            for permission in permission_classes
        ]

    def get_queryset(self):
        """
        لیست نظرات تایید شده محصول
        """

        return get_product_reviews(
            product_id=self.kwargs["product_pk"],
        )

    def get_object(self):
        """
        دریافت یک نظر
        """

        obj = get_review_by_id(
            review_id=self.kwargs["pk"],
        )

        self.check_object_permissions(
            self.request,
            obj,
        )

        return obj

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

    def update(self, request, *args, **kwargs):

        review = self.get_object()

        serializer = self.get_serializer(
            review,
            data=request.data,
            partial=kwargs.get(
                "partial",
                False,
            ),
        )

        serializer.is_valid(
            raise_exception=True,
        )

        review = update_review(
            review=review,
            **serializer.validated_data,
        )

        return Response(
            ReviewSerializer(review).data,
        )

    def destroy(self, request, *args, **kwargs):
        """
        حذف منطقی نظر
        """

        review = self.get_object()

        deactivate_review(
            review=review,
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )