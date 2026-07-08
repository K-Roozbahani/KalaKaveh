from rest_framework import serializers

from carts.models import (
    Cart,
    CartItem,
)

from discounts.services.price_engine import (
    calculate_variant_price,
)

from products.models import ProductVariant


# ==========================================================
# Cart Item Serializer
# ==========================================================

class CartItemSerializer(serializers.ModelSerializer):
    """
    نمایش اطلاعات هر آیتم سبد خرید.
    """

    variant_id = serializers.IntegerField(
        source="variant.id",
        read_only=True,
    )

    product_id = serializers.IntegerField(
        source="variant.product.id",
        read_only=True,
    )

    product_name = serializers.CharField(
        source="variant.product.name",
        read_only=True,
    )

    product_category = serializers.CharField(
        source="variant.product.category.name",
        read_only=True,
    )

    product_brand = serializers.CharField(
        source="variant.product.brand.name",
        read_only=True,
    )

    sku = serializers.CharField(
        source="variant.sku",
        read_only=True,
    )

    unit_price = serializers.SerializerMethodField()

    discount_amount = serializers.SerializerMethodField()

    final_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem

        fields = (
            "id",

            "variant_id",

            "product_id",
            "product_name",
            "product_category",
            "product_brand",

            "sku",

            "quantity",

            "unit_price",
            "discount_amount",
            "final_price",
        )

    # =====================================================
    # Price Snapshot Cache
    # =====================================================

    def _get_price_snapshot(self, obj):
        """
        دریافت PriceSnapshot با Cache در سطح Serializer
        """

        cache = getattr(
            self,
            "_price_snapshot_cache",
            None,
        )

        if cache is None:

            cache = {}

            self._price_snapshot_cache = cache

        if obj.variant_id not in cache:

            cache[obj.variant_id] = calculate_variant_price(
                variant=obj.variant,
            )

        return cache[obj.variant_id]

    def get_unit_price(self, obj):

        return self._get_price_snapshot(
            obj,
        ).base_price

    def get_discount_amount(self, obj):

        return self._get_price_snapshot(
            obj,
        ).discount_amount

    def get_final_price(self, obj):

        return self._get_price_snapshot(
            obj,
        ).final_price


# ==========================================================
# Cart Serializer
# ==========================================================

class CartSerializer(serializers.ModelSerializer):
    """
    نمایش اطلاعات سبد خرید.
    """

    items = CartItemSerializer(
        many=True,
        read_only=True,
    )

    items_count = serializers.SerializerMethodField()

    subtotal = serializers.SerializerMethodField()

    product_discount = serializers.SerializerMethodField()

    coupon_discount = serializers.SerializerMethodField()

    discount = serializers.SerializerMethodField()

    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart

        fields = (
            "id",

            "items_count",

            "subtotal",
            "product_discount",
            "coupon_discount",
            "discount",
            "total",

            "items",

            "created_at",
            "updated_at",
        )

    # =====================================================
    # Pricing Cache
    # =====================================================

    def _get_pricing(self):
        """
        دریافت خلاصه مالی سبد خرید
        """

        pricing = getattr(
            self,
            "_pricing",
            None,
        )

        if pricing is None:

            pricing = self.context["pricing"]

            self._pricing = pricing

        return pricing

    def get_items_count(self, obj):

        return self._get_pricing()["items_count"]

    def get_subtotal(self, obj):

        return self._get_pricing()["subtotal"]

    def get_product_discount(self, obj):

        return self._get_pricing()["product_discount"]

    def get_coupon_discount(self, obj):

        return self._get_pricing()["coupon_discount"]

    def get_discount(self, obj):

        return self._get_pricing()["discount"]

    def get_total(self, obj):

        return self._get_pricing()["total"]


# ==========================================================
# Add Cart Item
# ==========================================================

class AddCartItemSerializer(serializers.Serializer):
    """
    Serializer افزودن کالا به سبد خرید.
    """

    variant = serializers.PrimaryKeyRelatedField(
        queryset=ProductVariant.objects.filter(
            is_active=True,
        ),
    )

    quantity = serializers.IntegerField(
        min_value=1,
    )


# ==========================================================
# Update Cart Item
# ==========================================================

class UpdateCartItemSerializer(serializers.Serializer):
    """
    Serializer تغییر تعداد کالا.
    """

    quantity = serializers.IntegerField(
        min_value=1,
    )