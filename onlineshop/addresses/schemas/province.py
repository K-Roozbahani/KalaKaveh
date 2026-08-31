"""
Schemaهای OpenAPI مربوط به استان‌ها.
"""

from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)

from addresses.api.serializers import (
    ProvinceWithCitiesSerializer,
)


province_schema = extend_schema_view(
    list=extend_schema(
        summary="لیست استان‌ها",
        description=(
            "دریافت لیست تمام استان‌ها به همراه شهرهای "
            "زیرمجموعه هر استان."
        ),
        responses={
            200: OpenApiResponse(
                response=ProvinceWithCitiesSerializer(many=True),
                description="لیست استان‌ها به همراه شهرها.",
            ),
        },
    ),
)