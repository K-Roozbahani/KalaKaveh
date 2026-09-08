from drf_spectacular.utils import extend_schema, extend_schema_view

from discounts.api.serializers.discount import (
    DiscountListSerializer,
    DiscountDetailSerializer,
)


discount_schema = extend_schema_view(
    list=extend_schema(
        summary="لیست تخفیف‌ها",
        description=(
            "دریافت لیست تخفیف‌های فعال و معتبر."
        ),
        responses={
            200: DiscountListSerializer(many=True),
        },
        tags=["تخفیف"],
    ),
    retrieve=extend_schema(
        summary="جزئیات تخفیف",
        description=(
            "دریافت جزئیات یک تخفیف فعال بر اساس slug "
            "به همراه محدوده‌های اعمال تخفیف."
        ),
        responses={
            200: DiscountDetailSerializer,
        },
        tags=["تخفیف"],
    ),
)