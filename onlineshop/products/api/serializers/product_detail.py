from rest_framework import serializers

from products.models import Product
from .attribute import ProductAttributeValueSerializer

from .brand import BrandSerializer
from .category import CategorySerializer
from .image import ProductImageSerializer
from .variant import VariantSerializer
from .review import ReviewSerializer


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    نمایش جزئیات محصول
    """

    brand = BrandSerializer(
        read_only=True,
    )

    category = CategorySerializer(
        read_only=True,
    )

    images = ProductImageSerializer(
        many=True,
        read_only=True,
    )

    variants = VariantSerializer(
        many=True,
        read_only=True,
    )

    reviews = ReviewSerializer(
        many=True,
        read_only=True,
    )

    attributes = ProductAttributeValueSerializer(
        source='attribute_values',
        many=True,
        read_only=True,
    )

    class Meta:
        model = Product

        fields = (
            "id",
            "name",
            "slug",
            "description",
            "brand",
            "category",
            "images",
            'attributes',
            "variants",
            "reviews",
        )

        read_only_fields = fields