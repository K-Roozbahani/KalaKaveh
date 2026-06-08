from rest_framework import serializers

from discounts.models import CouponUsage


class CouponUsageSerializer(
    serializers.ModelSerializer
):

    user_phone = serializers.CharField(
        source="user.phone_number",
        read_only=True
    )

    coupon_code = serializers.CharField(
        source="coupon.code",
        read_only=True
    )

    class Meta:
        model = CouponUsage
        fields = (
            "id",
            "coupon",
            "coupon_code",
            "user",
            "user_phone",
            "order",
            "used_at",
        )

        read_only_fields = (
            "used_at",
        )