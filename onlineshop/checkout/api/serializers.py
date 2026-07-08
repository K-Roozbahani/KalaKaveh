from rest_framework import serializers

from payments.constants import GatewayType


# =====================================================
# Checkout
# =====================================================

class CheckoutSerializer(serializers.Serializer):
    """
    دریافت اطلاعات Checkout و اعمال تغییرات انتخاب‌های کاربر.
    """

    address_id = serializers.IntegerField(
        required=False,
        min_value=1,
    )

    shipping_method_id = serializers.IntegerField(
        required=False,
        min_value=1,
    )

    coupon_code = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=50,
    )


# =====================================================
# Checkout Confirm
# =====================================================

class CheckoutConfirmSerializer(serializers.Serializer):
    """
    تایید نهایی Checkout.
    """

    gateway_type = serializers.ChoiceField(
        choices=GatewayType.choices,
    )

    note = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
    )