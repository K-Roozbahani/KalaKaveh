from rest_framework import serializers

from products.models import (
    ProductImage,
    VariantImage,
)


class ProductImageSerializer(serializers.ModelSerializer):
    """
    تصاویر محصول
    """

    class Meta:
        model = ProductImage

        fields = (
            "id",
            "image",
            "alt_text",
            "is_primary",
        )

        read_only_fields = fields


class VariantImageSerializer(serializers.ModelSerializer):
    """
    تصاویر تنوع محصول
    """

    class Meta:
        model = VariantImage

        fields = (
            "id",
            "image",
            "is_primary",
        )

        read_only_fields = fields