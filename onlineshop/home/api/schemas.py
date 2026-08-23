"""
Schemaهای OpenAPI مربوط به صفحه اصلی فروشگاه.
"""

from drf_spectacular.utils import (
    extend_schema,
)

from home.api.serializers import HomePageSerializer


schema_home_page = extend_schema(
    summary="دریافت اطلاعات صفحه اصلی",
    description=(
        "دریافت سکشن‌های فعال صفحه اصلی فروشگاه."
    ),
    responses={
        200: HomePageSerializer,
    },
    tags=["صفحه اصلی"],
)