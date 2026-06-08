from rest_framework import serializers

from discounts.models import (
    Discount,
    DiscountTarget
)

from .target import (
    DiscountTargetSerializer
)


class DiscountListSerializer(
    serializers.ModelSerializer
):

    targets_count = serializers.SerializerMethodField()

    class Meta:
        model = Discount
        fields = (
            "id",
            "name",
            "discount_type",
            "value",
            "priority",
            "is_active",
            "start_date",
            "end_date",
            "targets_count",
        )

    def get_targets_count(self, obj):
        return obj.targets.count()



class DiscountDetailSerializer(
    serializers.ModelSerializer
):

    targets = DiscountTargetSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Discount
        fields = "__all__"


class DiscountCreateUpdateSerializer(
    serializers.ModelSerializer
):

    targets = DiscountTargetSerializer(
        many=True,
        write_only=True
    )

    class Meta:
        model = Discount
        fields = (
            "id",
            "name",
            "discount_type",
            "value",
            "priority",
            "is_active",
            "start_date",
            "end_date",
            "targets",
        )

    def create(self, validated_data):

        targets_data = validated_data.pop(
            "targets",
            []
        )

        discount = Discount.objects.create(
            **validated_data
        )

        DiscountTarget.objects.bulk_create([
            DiscountTarget(
                discount=discount,
                **target
            )
            for target in targets_data
        ])

        return discount

    def create(self, validated_data):

        targets_data = validated_data.pop(
            "targets",
            []
        )

        discount = Discount.objects.create(
            **validated_data
        )

        DiscountTarget.objects.bulk_create([
            DiscountTarget(
                discount=discount,
                **target
            )
            for target in targets_data
        ])

        return discount

    