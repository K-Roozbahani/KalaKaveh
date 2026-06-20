from rest_framework import serializers

from orders.models import Order, OrderItem


class OrderBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer for order serializers.
    """

    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    class Meta:
        model = Order
        fields = (
            "id",
            "order_number",
            "status",
            "status_display",
        )
        read_only_fields = fields


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Order item serializer.
    """

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


class OrderListSerializer(OrderBaseSerializer):
    """
    Order list serializer.
    """

    items_count = serializers.IntegerField(
        source="items.count",
        read_only=True,
    )

    class Meta(OrderBaseSerializer.Meta):
        fields = (
            *OrderBaseSerializer.Meta.fields,

            "total_amount",

            "items_count",

            "created_at",
        )

        read_only_fields = fields


class OrderDetailSerializer(OrderBaseSerializer):
    """
    Order detail serializer.
    """

    items = OrderItemSerializer(
        many=True,
        read_only=True,
    )

    shipping_method_name = serializers.SerializerMethodField()

    class Meta(OrderBaseSerializer.Meta):
        fields = (
            *OrderBaseSerializer.Meta.fields,

            "address_snapshot",

            "subtotal",
            "discount_amount",
            "shipping_method_snapshot",
            "shipping_method_name",
            "shipping_cost",
            "total_amount",

            "note",

            "items",

            "created_at",
            "updated_at",
        )

        read_only_fields = fields

    def get_shipping_method_name(
            self,
            obj,
    ):
        return (
            obj.shipping_method_snapshot.get(
                "name"
            )
        )


class CreateOrderSerializer(serializers.Serializer):
    """
    Create order serializer.
    """

    address_id = serializers.IntegerField(
        min_value=1,
    )
    shipping_method_id = serializers.IntegerField(
        min_value=1,
    )

    note = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
    )