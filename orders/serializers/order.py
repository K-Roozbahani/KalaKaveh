from rest_framework import serializers

from orders.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem

        fields = (
            "id",
            "quantity",
            "price",
            "discount_amount",
            "final_price",
            "product_snapshot",
        )

        read_only_fields = fields


class OrderListSerializer(serializers.ModelSerializer):
    items_count = serializers.IntegerField(
        source="items.count",
        read_only=True,
    )

    class Meta:
        model = Order

        fields = (
            "id",
            "order_number",
            "status",
            "total_amount",
            "items_count",
            "created_at",
        )

        read_only_fields = fields


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Order

        fields = (
            "id",
            "order_number",
            "status",

            "address_snapshot",

            "subtotal",
            "discount_amount",
            "shipping_cost",
            "total_amount",

            "note",

            "items",

            "created_at",
            "updated_at",
        )

        read_only_fields = fields


class CreateOrderSerializer(serializers.Serializer):
    address_id = serializers.IntegerField(
        min_value=1,
    )

    note = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
    )