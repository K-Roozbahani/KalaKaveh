from rest_framework import serializers

from discounts.models import Coupon

class CouponSerializer(
    serializers.ModelSerializer
):

    discount_name = serializers.CharField(
        source="discount.name",
        read_only=True
    )

    class Meta:
        model = Coupon
        fields = (
            "id",
            "code",
            "discount",
            "discount_name",
            "usage_limit",
            "used_count",
            "is_active",
            "start_date",
            "end_date",
        )

        read_only_fields = (
            "used_count",
        )


