from rest_framework import serializers
from django.core.exceptions import ValidationError

from products.models import ProductVariant

from .image import VariantImageSerializer
from .attribute import ProductVariantAttributeSerializer
from ...services.stock import ensure_variant_can_be_purchased


class VariantSerializer(serializers.ModelSerializer):
    """
    نمایش اطلاعات تنوع محصول
    """

    images = VariantImageSerializer(
        many=True,
        read_only=True,
    )

    has_stock = serializers.SerializerMethodField()

    attributes = ProductVariantAttributeSerializer(
        source="prefetched_attributes",
        many=True,
        read_only=True,
    )

    class Meta:
        model = ProductVariant

        fields = (
            "id",
            "sku",
            "price",
            "discount_amount",
            "final_price",
            "stock",
            "has_stock",
            "images",
            "attributes",
        )

        read_only_fields = fields

    def get_has_stock(self, obj):
        """
        بررسی امکان خرید تنوع محصول.
        """

        try:
            ensure_variant_can_be_purchased(
                variant=obj,
            )
        except ValidationError:
            return False

        return True