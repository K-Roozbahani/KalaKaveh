from rest_framework import serializers

from products.models import ProductVariant

from .image import VariantImageSerializer


class VariantSerializer(serializers.ModelSerializer):
    """
    نمایش اطلاعات تنوع محصول
    """

    images = VariantImageSerializer(
        many=True,
        read_only=True,
    )

    has_stock = serializers.SerializerMethodField()

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
        )

        read_only_fields = fields

    def get_has_stock(
        self,
        obj,
    ):
        """
        بررسی موجود بودن تنوع
        """

        return (
            obj.is_active and
            obj.stock > 0
        )