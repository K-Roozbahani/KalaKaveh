from rest_framework import serializers

from shipping.models import (
    ShippingMethod,
    Shipment,
)


class ShippingMethodSerializer(
    serializers.ModelSerializer,
):
    class Meta:
        model = ShippingMethod

        fields = (
            "id",
            "name",
            "price",
            "estimated_days",
        )

        read_only_fields = fields


class ShipmentListSerializer(
    serializers.ModelSerializer,
):
    shipping_method_name = (
        serializers.CharField(
            source="shipping_method.name",
            read_only=True,
        )
    )

    order_number = serializers.CharField(
        source="order.order_number",
        read_only=True,
    )

    class Meta:
        model = Shipment

        fields = (
            "id",

            "order_number",

            "shipping_method_name",

            "tracking_code",

            "status",

            "shipped_at",
            "delivered_at",

            "created_at",
        )

        read_only_fields = fields


class ShipmentDetailSerializer(
    serializers.ModelSerializer,
):
    shipping_method = (
        ShippingMethodSerializer(
            read_only=True,
        )
    )

    order_number = serializers.CharField(
        source="order.order_number",
        read_only=True,
    )

    class Meta:
        model = Shipment

        fields = (
            "id",

            "order_number",

            "shipping_method",

            "tracking_code",

            "status",

            "description",

            "shipped_at",
            "delivered_at",

            "created_at",
            "updated_at",
        )

        read_only_fields = fields