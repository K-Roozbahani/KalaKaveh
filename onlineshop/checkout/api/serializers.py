from rest_framework import serializers

from addresses.api.serializers import AddressDetailSerializer

from carts.api.serializers import CartSerializer

from discounts.api.serializers.coupon import CouponSerializer

from payments.constants import GatewayType

from shipping.serializers import ShippingMethodSerializer


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


class CheckoutSummarySerializer(serializers.Serializer):
    """
    Serializer خروجی اطلاعات Checkout.
    """

    cart = CartSerializer(
        help_text="اطلاعات سبد خرید فعال.",
    )

    address = AddressDetailSerializer(
        allow_null=True,
        help_text="آدرس انتخاب‌شده برای ارسال.",
    )

    shipping_method = ShippingMethodSerializer(
        allow_null=True,
        help_text="روش ارسال انتخاب‌شده.",
    )

    shipping_methods = ShippingMethodSerializer(
        many=True,
        help_text="روش‌های ارسال قابل انتخاب.",
    )

    coupon = CouponSerializer(
        allow_null=True,
        help_text="کوپن اعمال‌شده.",
    )

    shipping_cost = serializers.IntegerField(
        help_text="هزینه ارسال.",
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