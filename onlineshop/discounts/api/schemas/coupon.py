"""
Schemaهای OpenAPI مربوط به کد تخفیف.
"""

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

from discounts.api.serializers.coupon import (
    CouponCheckSerializer,
    CouponSerializer,
)


coupon_schema = extend_schema_view(
    check=extend_schema(
        summary="بررسی کد تخفیف",
        description=(
            "بررسی اعتبار کد تخفیف برای کاربر جاری. "
            "در صورت معتبر بودن، اطلاعات کد تخفیف "
            "برگردانده می‌شود."
        ),
        request=CouponCheckSerializer,
        responses={
            200: CouponSerializer,
        },
        tags=["تخفیف"],
    ),
)