from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from payments.models import Payment
from payments.constants import GatewayType


class PaymentCreateSerializer(serializers.Serializer):
    order_number = serializers.CharField(
        label=_("شماره سفارش"),
    )

    gateway = serializers.ChoiceField(
        label=_("درگاه پرداخت"),
        choices=GatewayType.choices,
    )


class PaymentListSerializer(
    serializers.ModelSerializer
):
    order_number = serializers.CharField(
        source="order.order_number",
        read_only=True,
    )

    class Meta:
        model = Payment

        fields = (
            "id",
            "order_number",
            "gateway",
            "amount",
            "status",
            "paid_at",
            "created_at",
        )


class PaymentDetailSerializer(
    serializers.ModelSerializer
):
    order_number = serializers.CharField(
        source="order.order_number",
        read_only=True,
    )

    class Meta:
        model = Payment

        fields = (
            "id",

            "order_number",

            "gateway",

            "authority",
            "ref_id",

            "amount",

            "status",

            "failure_reason",

            "paid_at",

            "created_at",
            "updated_at",
        )


