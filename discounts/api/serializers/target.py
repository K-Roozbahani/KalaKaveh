from rest_framework import serializers

from discounts.models import DiscountTarget


class DiscountTargetSerializer(serializers.ModelSerializer):

    class Meta:
        model = DiscountTarget
        fields = (
            "id",
            "product",
            "variant",
            "category",
            "brand",
        )

    def validate(self, attrs):

        targets = [
            attrs.get("product"),
            attrs.get("variant"),
            attrs.get("category"),
            attrs.get("brand"),
        ]

        filled = len([
            item
            for item in targets
            if item is not None
        ])

        if filled != 1:
            raise serializers.ValidationError(
                "فقط یکی از فیلدهای product, variant, category, brand باید مقدار داشته باشد."
            )

        return attrs


