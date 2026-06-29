from rest_framework import serializers

from carts.models import Cart, CartItem
from products.models import ProductVariant


# ==========================================================
# Serializer نمایش آیتم سبد خرید
# ==========================================================
class CartItemSerializer(serializers.ModelSerializer):
    """
    نمایش اطلاعات هر آیتم سبد خرید.

    نکته:
        قیمت‌ها از ProductVariant خوانده می‌شوند
        و داخل CartItem ذخیره نمی‌شوند.
    """

    # شناسه Variant
    variant_id = serializers.IntegerField(
        source="variant.id",
        read_only=True,
    )

    # اطلاعات محصول
    product_id = serializers.IntegerField(
        source="variant.product.id",
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

    product_name = serializers.CharField(
        source="variant.product.name",
        read_only=True,
    )

    sku = serializers.CharField(
        source="variant.sku",
        read_only=True,
    )

    # قیمت‌های جاری Variant
    unit_price = serializers.DecimalField(
        source="variant.price",
        max_digits=12,
        decimal_places=0,
        read_only=True,
    )

    discount_amount = serializers.DecimalField(
        source="variant.discount_amount",
        max_digits=12,
        decimal_places=0,
        read_only=True,
    )

    final_price = serializers.DecimalField(
        source="variant.final_price",
        max_digits=12,
        decimal_places=0,
        read_only=True,
    )

    class Meta:
        model = CartItem

        fields = (
            "id",

            "variant_id",

            "product_id",
            "product_category",
            "product_brand",
            "product_name",

            "sku",

            "quantity",

            "unit_price",
            "discount_amount",
            "final_price",
        )


# ==========================================================
# Serializer نمایش سبد خرید
# ==========================================================
class CartSerializer(serializers.ModelSerializer):
    """
    نمایش اطلاعات سبد خرید.

    تمام محاسبات مالی توسط Service انجام می‌شود.
    """

    items = CartItemSerializer(
        many=True,
        read_only=True,
    )

    coupon_code = serializers.CharField(
        source="coupon.code",
        read_only=True,
    )

    items_count = serializers.IntegerField(
        read_only=True,
    )

    subtotal = serializers.DecimalField(
        max_digits=14,
        decimal_places=0,
        read_only=True,
    )

    product_discount = serializers.DecimalField(
        max_digits=14,
        decimal_places=0,
        read_only=True,
    )

    coupon_discount = serializers.DecimalField(
        max_digits=14,
        decimal_places=0,
        read_only=True,
    )

    discount_amount = serializers.DecimalField(
        max_digits=14,
        decimal_places=0,
        read_only=True,
    )

    total = serializers.DecimalField(
        max_digits=14,
        decimal_places=0,
        read_only=True,
    )

    class Meta:
        model = Cart

        fields = (
            "id",

            "coupon_code",

            "items_count",

            "subtotal",
            "product_discount",
            "coupon_discount",
            "discount_amount",
            "total",

            "items",

            "created_at",
            "updated_at",
        )


# ==========================================================
# افزودن کالا به سبد خرید
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

    def validate(self, attrs):

        variant = attrs["variant"]

        quantity = attrs["quantity"]

        if quantity > variant.stock:
            raise serializers.ValidationError(
                {
                    "quantity": (
                        "تعداد درخواستی بیشتر از موجودی کالا است."
                    )
                }
            )

        return attrs


# ==========================================================
# تغییر تعداد کالا
# ==========================================================
class UpdateCartItemSerializer(serializers.Serializer):
    """
    Serializer تغییر تعداد کالا.
    """

    quantity = serializers.IntegerField(
        min_value=1,
    )

    def validate_quantity(self, value):

        cart_item = self.context["cart_item"]

        if value > cart_item.variant.stock:
            raise serializers.ValidationError(
                "تعداد درخواستی بیشتر از موجودی کالا است."
            )

        return value


# ==========================================================
# اعمال کد تخفیف
# ==========================================================
class ApplyCouponSerializer(serializers.Serializer):
    """
    Serializer اعمال کد تخفیف.
    """

    code = serializers.CharField(
        max_length=100,
    )

    def validate_code(self, value):

        value = value.strip().upper()

        if not value:
            raise serializers.ValidationError(
                "کد تخفیف معتبر نیست."
            )

        return value