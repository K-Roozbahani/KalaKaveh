from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

from products.api.serializers.review import (
    ReviewSerializer,
    ReviewWriteSerializer,
)
from products.selectors import (
    get_product_by_slug,
    get_product_reviews,
    get_review_by_id,
)
from products.services.review import (
    create_review,
    deactivate_review,
    update_review,
)
from products.validators import (
    validate_review_product,
)
from utils.api.views import BaseGenericViewSet
from utils.permissions import IsOwnerOrAdmin


@extend_schema_view(
    list=extend_schema(
        summary="لیست نظرات",
        description="دریافت لیست نظرات تایید شده محصول",
        responses=ReviewSerializer,
    ),
    retrieve=extend_schema(
        summary="جزئیات نظر",
        description="دریافت جزئیات نظر ثبت شده توسط کاربر",
        responses=ReviewSerializer,
    ),
    create=extend_schema(
        summary="ثبت نظر",
        description="ثبت نظر جدید برای محصول",
        request=ReviewWriteSerializer,
        responses=ReviewSerializer,
    ),
    update=extend_schema(
        summary="بروزرسانی نظر",
        description="بروزرسانی کامل نظر ثبت شده توسط کاربر",
        request=ReviewWriteSerializer,
        responses=ReviewSerializer,
    ),
    partial_update=extend_schema(
        summary="ویرایش نظر",
        description="ویرایش بخشی از نظر ثبت شده توسط کاربر",
        request=ReviewWriteSerializer,
        responses=ReviewSerializer,
    ),
    destroy=extend_schema(
        summary="حذف نظر",
        description="حذف منطقی نظر ثبت شده توسط کاربر",
    ),
)
@extend_schema(
    tags=["review"],
)
class ReviewViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    BaseGenericViewSet,
):
    """
    مدیریت نظرات محصولات
    """

    def get_permissions(self):
        """
        تعیین سطح دسترسی بر اساس عملیات
        """

        if self.action == "list":
            permission_classes = (
                AllowAny,
            )

        elif self.action == "create":
            permission_classes = (
                IsAuthenticated,
            )

        else:
            permission_classes = (
                IsOwnerOrAdmin,
            )

        return [
            permission()
            for permission in permission_classes
        ]

    def get_product(self):
        """
        دریافت محصول بر اساس slug
        """

        return get_product_by_slug(
            slug=self.kwargs["product_slug"],
        )

    def get_queryset(self):
        """
        دریافت نظرات تایید شده محصول
        """

        product = self.get_product()

        return get_product_reviews(
            product_id=product.id,
        )

    def get_object(self):
        """
        دریافت نظر متعلق به محصول جاری
        """

        product = self.get_product()

        review = get_review_by_id(
            review_id=self.kwargs["pk"],
        )

        if review is None:
            raise NotFound(
                _("نظر موردنظر یافت نشد.")
            )

        try:
            validate_review_product(
                review=review,
                product=product,
            )
        except ValidationError as exc:
            raise NotFound(
                _("نظر موردنظر یافت نشد.")
            ) from exc

        self.check_object_permissions(
            self.request,
            review,
        )

        return review

    def get_serializer_class(self):
        """
        تعیین Serializer بر اساس عملیات
        """

        if self.action in (
            "create",
            "update",
            "partial_update",
        ):
            return ReviewWriteSerializer

        return ReviewSerializer

    def create(
        self,
        request,
        *args,
        **kwargs,
    ):
        """
        ثبت نظر جدید
        """

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        review = create_review(
            product=self.get_product(),
            user=request.user,
            **serializer.validated_data,
        )

        response_serializer = ReviewSerializer(
            review,
            context=self.get_serializer_context(),
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def update(
        self,
        request,
        *args,
        **kwargs,
    ):
        """
        بروزرسانی کامل نظر
        """

        review = self.get_object()

        serializer = self.get_serializer(
            review,
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        review = update_review(
            review=review,
            **serializer.validated_data,
        )

        response_serializer = ReviewSerializer(
            review,
            context=self.get_serializer_context(),
        )

        return Response(
            response_serializer.data,
        )

    def partial_update(
        self,
        request,
        *args,
        **kwargs,
    ):
        """
        بروزرسانی بخشی از نظر
        """

        review = self.get_object()

        serializer = self.get_serializer(
            review,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        review = update_review(
            review=review,
            **serializer.validated_data,
        )

        response_serializer = ReviewSerializer(
            review,
            context=self.get_serializer_context(),
        )

        return Response(
            response_serializer.data,
        )

    def destroy(
        self,
        request,
        *args,
        **kwargs,
    ):
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