from rest_framework import serializers

from payments.constants import GatewayType


class CheckoutSerializer(serializers.Serializer):
    """
    Serializer دریافت اطلاعات Checkout.
    """

    cart = serializers.DictField(read_only=True)

    addresses = serializers.ListField(
        read_only=True,
    )

    shipping_methods = serializers.ListField(
        read_only=True,
    )

    totals = serializers.DictField(
        read_only=True,
    )


class CheckoutCreateSerializer(serializers.Serializer):
    """
    Serializer ایجاد Checkout.
    """

    address_id = serializers.IntegerField(
        required=True,
    )

    shipping_method_id = serializers.IntegerField(
        required=True,
    )

    gateway = serializers.ChoiceField(
        choices=GatewayType.choices,
    )

    coupon = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    note = serializers.CharField(
        required=False,
        allow_blank=True,
    )