from rest_framework import serializers

from products.models import Product
from .attribute import ProductAttributeValueSerializer

from .brand import BrandSerializer
from .category import CategorySerializer
from .image import ProductImageSerializer
from .variant import VariantSerializer
from .review import ReviewSerializer, ReviewSummarySerializer
from ...selectors import get_product_review_summary


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    نمایش جزئیات محصول
    """

    brand = BrandSerializer(read_only=True)

    category = CategorySerializer(read_only=True)

    images = ProductImageSerializer(
        many=True,
        read_only=True,
    )

    variants = VariantSerializer(
        source="prefetched_variants",
        many=True,
        read_only=True,
    )

    attributes = ProductAttributeValueSerializer(
        source="prefetched_attribute_values",
        many=True,
        read_only=True,
    )

    highlight_attributes = ProductAttributeValueSerializer(
        source="highlight_attributes",
        many=True,
        read_only=True,
    )

    reviews = serializers.SerializerMethodField()

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
            "highlight_attributes",
            "attributes",
            "variants",
            "reviews",
        )

        read_only_fields = fields

    def get_reviews(self, obj):
        return ReviewSummarySerializer(
            get_product_review_summary(
                product_id=obj.id
            )
        ).data