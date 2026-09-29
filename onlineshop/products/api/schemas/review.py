from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

from products.api.serializers.review import (
    ReviewWriteSerializer,
    UserReviewsSerializer,
)


schema_user_review = extend_schema_view(
        list=extend_schema(
            summary="لیست نظرات کاربر",
            description="دریافت لیست نظرات ثبت‌شده توسط کاربر جاری.",
            responses=UserReviewsSerializer(many=True),
            tags=["review",],
        ),
        update=extend_schema(
            summary="ویرایش نظر کاربر",
            description="ویرایش کامل نظر ثبت‌شده توسط کاربر جاری.",
            request=ReviewWriteSerializer,
            responses=UserReviewsSerializer,
            tags=["review",],
        ),
        partial_update=extend_schema(
            summary="ویرایش بخشی از نظر کاربر",
            description="ویرایش بخشی از نظر ثبت‌شده توسط کاربر جاری.",
            request=ReviewWriteSerializer,
            responses=UserReviewsSerializer,
            tags=["review",],
        ),
    )