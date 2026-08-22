from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
    OpenApiTypes,
)


cart_schema = extend_schema_view(
    list=extend_schema(
        tags=["Cart"],
        summary="نمایش سبد خرید",
        responses={
            200: OpenApiResponse(
                response="carts.api.serializers.CartSerializer",
                description="اطلاعات کامل سبد خرید.",
            ),
        },
    ),
    clear=extend_schema(
        tags=["Cart"],
        summary="پاک کردن سبد خرید",
        request=None,
        responses={
            200: OpenApiResponse(
                response="carts.api.serializers.CartSerializer",
                description="سبد خرید پس از پاک شدن آیتم‌ها.",
            ),
        },
    ),
    count=extend_schema(
        tags=["Cart"],
        summary="دریافت تعداد کالاهای سبد خرید",
        description=(
            "تعداد کل کالاهای موجود در سبد خرید فعال را برمی‌گرداند. "
            "مقدار quantity تمام آیتم‌های سبد خرید با یکدیگر جمع می‌شود. "
            "در صورت نبودن سبد خرید، مقدار صفر برگردانده می‌شود."
        ),
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="تعداد کالاهای موجود در سبد خرید.",
            ),
        },
    ),
)