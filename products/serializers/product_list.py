from rest_framework import serializers

from products.models import Product

from .brand import BrandSerializer
from .category import CategorySerializer


class ProductListSerializer(serializers.ModelSerializer):
    """
    نمایش لیست محصولات
    """

    brand = BrandSerializer(
        read_only=True,
    )

    category = CategorySerializer(
        read_only=True,
    )

    primary_image = serializers.SerializerMethodField()

    has_stock = serializers.SerializerMethodField()

    class Meta:
        model = Product

        fields = (
            "id",
            "name",
            "slug",
            "brand",
            "category",
            "primary_image",
            "has_stock",
        )

        read_only_fields = fields

    def get_primary_image(
        self,
        obj,
    ):
        image = obj.images.first()

        if image:
            return image.image.url

        return None

    def get_has_stock(
        self,
        obj,
    ):
        return obj.variants.filter(
            is_active=True,
            stock__gt=0,
        ).exists()