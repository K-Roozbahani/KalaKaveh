from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)

from favorites.api.serializers.favorite import (
    FavoriteAddSerializer,
    FavoriteListSerializer,
)


favorite_schema = extend_schema_view(
    list=extend_schema(
        summary="لیست علاقه‌مندی‌ها",
        description="دریافت لیست محصولات مورد علاقه کاربر.",
        responses={
            200: FavoriteListSerializer(many=True),
        },
        tags=["علاقه‌مندی‌ها"],
    ),
    create=extend_schema(
        summary="افزودن به علاقه‌مندی‌ها",
        description="افزودن یک محصول به لیست علاقه‌مندی‌های کاربر.",
        request=FavoriteAddSerializer,
        responses={
            201: FavoriteListSerializer,
        },
        tags=["علاقه‌مندی‌ها"],
    ),
    destroy=extend_schema(
        summary="حذف از علاقه‌مندی‌ها",
        description="حذف یک محصول از لیست علاقه‌مندی‌های کاربر.",
        responses={
            204: OpenApiResponse(
                description="محصول با موفقیت از علاقه‌مندی‌ها حذف شد.",
            ),
        },
        tags=["علاقه‌مندی‌ها"],
    ),
)