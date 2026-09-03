"""
Viewهای مربوط به بررسی کد تخفیف.
"""

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from discounts.api.schemas.coupon import coupon_schema
from discounts.api.serializers.coupon import CouponCheckSerializer
from discounts.selectors import get_coupon_by_code
from discounts.services.coupon import validate_coupon


@coupon_schema
class CouponViewSet(GenericViewSet):
    """
    API مربوط به عملیات کد تخفیف.
    """

    permission_classes = [IsAuthenticated]

    @action(
        detail=False,
        methods=["post"],
        url_path="check",
    )
    def check(self, request):
        """
        بررسی اعتبار کد تخفیف برای کاربر جاری.
        """

        serializer = CouponCheckSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        coupon_code = serializer.validated_data["code"]

        coupon = get_coupon_by_code(
            code=coupon_code,
        )

        coupon = validate_coupon(
            coupon=coupon,
            user=request.user,
        )

        return Response(
            CouponCheckSerializer(coupon).data,
            status=status.HTTP_200_OK,
        )