from rest_framework import serializers

from products.api.serializers import ProductImageSerializer
from products.selectors import get_default_variant, get_primary_product_image
from products.services.stock import ensure_variant_can_be_purchased
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

    image = serializers.SerializerMethodField()

    price = serializers.SerializerMethodField()
    discount_amount = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    has_stock = serializers.SerializerMethodField()
    slug = serializers.CharField(
        source="product.slug",
        read_only=True,
    )

    class Meta:
        model = Favorite
        fields = [
            "id",
            "slug",
            "brand",
            "category",
            "name",
            "image",
            "has_stock",
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

    def get_has_stock(self, obj):
        """
        برسی میکند آیا مصحول موجو می باشد
        """
        variant = self._get_default_variant(obj)

        if variant is None:
            return False

        return True if variant.stock else False


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

    def get_image(self, obj):
        """
        دریافت URL کامل تصویر اصلی محصول.
        """

        image = get_primary_product_image(
            product=obj.product,
        )

        if not image:
            return None

        request = self.context.get("request")

        if not request:
            return image.image.url

        return request.build_absolute_uri(
            image.image.url,
        )


class FavoriteAddSerializer(serializers.Serializer):
    """
    Serializer افزودن محصول به علاقه‌مندی.
    """

    product_id = serializers.IntegerField(
        min_value=1,
        write_only=True,
        label="شناسه محصول",
    )


class FavoriteProductIDsSerializer(serializers.Serializer):
    """
    شناسه محصولات موجود در علاقه‌مندی‌های کاربر.
    """
    id = serializers.IntegerField(
        min_value=1,
        read_only=True,
        label="شناسه علاقه مندی",
    )

    product_id = serializers.IntegerField(
        min_value=1,
        read_only=True,
        label="شناسه محصول",
    )