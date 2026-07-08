from rest_framework import serializers

from products.models import Product
from products.selectors import get_default_variant, get_primary_product_image, get_primary_variant_image

from .brand import BrandSerializer
from .category import CategorySerializer


class ProductListSerializer(serializers.ModelSerializer):
    """
    نمایش لیست محصولات (بهینه شده برای production)
    """

    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    price = serializers.SerializerMethodField()
    discount_amount = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()
    has_stock = serializers.SerializerMethodField()

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product

        fields = (
            "id",
            "name",
            "slug",
            "brand",
            "category",
            "price",
            "discount_amount",
            "final_price",
            "has_stock",
            "image",
        )

        read_only_fields = fields

    # =====================================================
    # Default Variant Cache
    # =====================================================

    def _get_default_variant(self, obj):
        """
        گرفتن Variant پیش‌فرض با cache در سطح serializer
        """

        cache = getattr(self, "_default_variant_cache", None)

        if cache is None:
            cache = {}
            self._default_variant_cache = cache

        if obj.id in cache:
            return cache[obj.id]

        variant = get_default_variant(product=obj)

        cache[obj.id] = variant

        return variant

    # =====================================================
    # Fields
    # =====================================================

    def get_price(self, obj):
        variant = self._get_default_variant(obj)

        if not variant:
            return None

        return variant.price

    def get_discount_amount(self, obj):
        variant = self._get_default_variant(obj)

        if not variant:
            return None

        return variant.discount_amount

    def get_final_price(self, obj):
        variant = self._get_default_variant(obj)

        if not variant:
            return None

        return variant.final_price

    def get_has_stock(self, obj):
        variant = self._get_default_variant(obj)

        if not variant:
            return False

        return (
            variant.is_active and variant.stock > 0
        )

    def get_image(self, obj):

        image = get_primary_product_image(
            product=obj,
        )

        if image:
            return image.image.url

        return None