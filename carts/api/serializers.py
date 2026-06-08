from rest_framework import serializers

from carts.models import Cart, CartItem
from products.models import ProductVariant


# ==========================================
# Serializer نمایش آیتم سبد خرید
# ==========================================
class CartItemSerializer(serializers.ModelSerializer):
    """
    نمایش اطلاعات هر آیتم سبد خرید

    نکته:
    قیمت‌ها از ProductVariant خوانده می‌شوند
    و داخل CartItem ذخیره نمی‌شوند.
    """

    product_id = serializers.IntegerField(
        source="variant.product.id",
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

            # تنوع محصول انتخاب شده
            "variant",

            # اطلاعات نمایشی محصول
            "product_id",
            "product_name",
            "sku",

            # تعداد انتخاب شده
            "quantity",

            # قیمت‌های جاری
            "unit_price",
            "discount_amount",
            "final_price",
        )


# ==========================================
# Serializer نمایش کل سبد خرید
# ==========================================
class CartSerializer(serializers.ModelSerializer):
    """
    نمایش سبد خرید

    مقادیر زیر از Service یا Selector
    توسط annotate یا context تامین می‌شوند:

        items_count
        subtotal
        discount
        total

    بنابراین هیچ محاسبه‌ای داخل Serializer انجام نمی‌شود.
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

    discount = serializers.DecimalField(
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

            # خلاصه سبد
            "items_count",
            "subtotal",
            "discount",
            "total",

            # آیتم‌ها
            "items",

            "created_at",
            "updated_at",
        )


# ==========================================
# افزودن کالا به سبد
# ==========================================
class AddCartItemSerializer(serializers.Serializer):
    """
    ورودی API:

    POST /cart/items/

    {
        "variant_id": 1,
        "quantity": 2
    }
    """

    variant_id = serializers.IntegerField()

    quantity = serializers.IntegerField(
        min_value=1,
    )

    def validate_variant_id(self, value):
        """
        بررسی وجود Variant
        """

        try:
            variant = ProductVariant.objects.get(
                pk=value,
            )

        except ProductVariant.DoesNotExist:
            raise serializers.ValidationError(
                "تنوع محصول یافت نشد."
            )

        # اگر محصول غیرفعال شده باشد
        if hasattr(variant, "is_active"):
            if not variant.is_active:
                raise serializers.ValidationError(
                    "این محصول در حال حاضر قابل خرید نیست."
                )

        return value

    def validate(self, attrs):
        """
        بررسی موجودی کالا
        """

        variant = ProductVariant.objects.get(
            pk=attrs["variant_id"]
        )

        quantity = attrs["quantity"]

        if quantity > variant.stock:
            raise serializers.ValidationError(
                {
                    "quantity": "موجودی کافی نیست."
                }
            )

        return attrs


# ==========================================
# تغییر تعداد کالا
# ==========================================
class UpdateCartItemSerializer(serializers.Serializer):
    """
    PATCH /cart/items/{id}/

    {
        "quantity": 5
    }
    """

    quantity = serializers.IntegerField(
        min_value=1,
    )

    def validate_quantity(self, value):
        """
        بررسی موجودی هنگام تغییر تعداد
        """

        cart_item = self.context["cart_item"]

        if value > cart_item.variant.stock:
            raise serializers.ValidationError(
                "موجودی کافی نیست."
            )

        return value


# ==========================================
# اعمال کد تخفیف
# ==========================================
class ApplyCouponSerializer(serializers.Serializer):
    """
    POST /cart/apply-coupon/

    {
        "code": "WELCOME20"
    }
    """

    code = serializers.CharField(
        max_length=100,
    )

    def validate_code(self, value):
        """
        اعتبارسنجی اولیه کد تخفیف

        اعتبارسنجی کامل شامل:
            - فعال بودن
            - تاریخ شروع
            - تاریخ پایان
            - سقف استفاده
            - تعداد استفاده کاربر

        بهتر است در Service انجام شود.
        """

        value = value.strip().upper()

        if not value:
            raise serializers.ValidationError(
                "کد تخفیف معتبر نیست."
            )

        return value