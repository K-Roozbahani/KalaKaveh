from rest_framework import serializers

from discounts.models import Discount, DiscountScope

from .target import DiscountTargetSerializer


class DiscountListSerializer(serializers.ModelSerializer):
    targets_count = serializers.IntegerField(
        source="scopes.count",
        read_only=True,
    )

    class Meta:
        model = Discount
        fields = (
            "id",
            "name",
            "slug",
            "discount_type",
            "value",
            "priority",
            "is_active",
            "start_date",
            "end_date",
            "targets_count",
        )


class DiscountDetailSerializer(serializers.ModelSerializer):
    scopes = DiscountTargetSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Discount
        fields = (
            "id",
            "name",
            "slug",
            "discount_type",
            "value",
            "priority",
            "is_active",
            "start_date",
            "end_date",
            "scopes",
        )


class DiscountCreateUpdateSerializer(serializers.ModelSerializer):
    scopes = DiscountTargetSerializer(
        many=True,
        write_only=True,
        required=False,
    )

    class Meta:
        model = Discount
        fields = (
            "id",
            "name",
            "slug",
            "discount_type",
            "value",
            "priority",
            "is_active",
            "start_date",
            "end_date",
            "scopes",
        )

    def create(self, validated_data):
        scopes_data = validated_data.pop("scopes", [])

        discount = Discount.objects.create(
            **validated_data,
        )

        DiscountScope.objects.bulk_create(
            [
                DiscountScope(
                    discount=discount,
                    **scope,
                )
                for scope in scopes_data
            ]
        )

        return discount