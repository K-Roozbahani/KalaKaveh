from rest_framework import serializers

from products.selectors import get_default_variant

from favorites.models import Favorite


class FavoriteListSerializer(serializers.ModelSerializer):
    """
    Serializer نمایش لیست علاقه‌مندی‌های کاربر.
    """

    brand = serializers.CharField(
        source="product.brand.name",
        read_only=True,
    )

    category = serializers.CharField(
        source="product.category.name",
        read_only=True,
    )

    name = serializers.CharField(
        source="product.name",
        read_only=True,
    )

    price = serializers.SerializerMethodField()
    discount_amount = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = [
            "id",
            "brand",
            "category",
            "name",
            "price",
            "discount_amount",
            "total",
        ]

    def _get_default_variant(self, obj):
        """
        دریافت Variant پیش‌فرض محصول.

        Variantها در Selector قبلاً Prefetch شده‌اند و
        این تابع Query جدیدی ایجاد نمی‌کند.
        """

        return get_default_variant(
            product=obj.product,
        )

    def get_price(self, obj):
        """
        دریافت قیمت اصلی محصول.
        """

        variant = self._get_default_variant(obj)

        if variant is None:
            return None

        return variant.price

    def get_discount_amount(self, obj):
        """
        دریافت مبلغ تخفیف محصول.
        """

        variant = self._get_default_variant(obj)

        if variant is None:
            return None

        return variant.discount_amount

    def get_total(self, obj):
        """
        دریافت قیمت نهایی محصول.
        """

        variant = self._get_default_variant(obj)

        if variant is None:
            return None

        return variant.final_price


class FavoriteAddSerializer(serializers.Serializer):
    """
    Serializer افزودن محصول به علاقه‌مندی.
    """

    product_id = serializers.IntegerField(
        min_value=1,
        write_only=True,
        label="شناسه محصول",
    )