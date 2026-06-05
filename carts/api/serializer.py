# cart/serializers.py

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum # برای جمع در CartDetailSerializer

# وارد کردن مدل‌های لازم
from products.models import Product, ProductAttributeValue
from carts.models import Cart, CartItem, CartItemAttribute

# -----------------------------------------------------------------------------
# Serializers برای خواندن داده‌ها (نمایش سبد خرید)
# -----------------------------------------------------------------------------

class CartItemAttributeSerializer(serializers.ModelSerializer):
    """
    Serializer برای نمایش ویژگی‌های انتخاب شده برای یک آیتم سبد خرید.
    """
    # نمایش نام ویژگی (مثلاً "رنگ") و مقدار آن (مثلاً "قرمز")
    attribute_name = serializers.CharField(source='attribute_value.attribute.name', read_only=True)
    attribute_value_name = serializers.CharField(source='attribute_value.value', read_only=True)

    class Meta:
        model = CartItemAttribute
        fields = ['id', 'attribute_value', 'attribute_name', 'attribute_value_name']
        read_only_fields = ['id', 'attribute_value', 'attribute_name', 'attribute_value_name']


class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer برای نمایش یک آیتم منفرد در سبد خرید.
    """
    # نمایش ویژگی‌های انتخاب شده برای این آیتم به صورت لیست تودرتو
    item_attributes = CartItemAttributeSerializer(many=True, read_only=True)

    # نام محصول به صورت Snapshot شده در زمان افزودن به سبد
    product_name = serializers.CharField(source='product_name_snapshot', read_only=True)

    # نمایش URL عکس اصلی محصول با استفاده از فیلد main_image در مدل Product
    # چون main_image یک ImageField در Product است، اینجا به درستی نمایش داده می‌شود.
    product_image = serializers.ImageField(source='product.main_image', read_only=True)

    # قیمت کل برای این ردیف (تعداد * قیمت واحد) - این فیلد از property 'total_price' مدل CartItem می‌آید
    line_total = serializers.DecimalField(source='total_price', max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = [
            'id',
            'product',          # شناسه محصول اصلی (Product ID)
            'product_name',     # نام محصول (Snapshot شده)
            'product_image',    # URL عکس اصلی محصول
            'quantity',         # تعداد این آیتم
            'unit_price',       # قیمت واحد در زمان اضافه شدن به سبد (snapshot)
            'line_total',       # قیمت کل این ردیف (unit_price * quantity)
            'item_attributes',  # لیست ویژگی‌های انتخاب شده مرتبط با این آیتم
            'created_at',
            'updated_at',
        ]
        # فیلدهایی که نباید توسط کلاینت قابل تغییر باشند (برای عملیات GET)
        read_only_fields = [
            'id',
            'product',
            'product_name',
            'product_image',
            'unit_price',
            'line_total',
            'item_attributes',
            'created_at',
            'updated_at',
        ]


class CartDetailSerializer(serializers.ModelSerializer):
    """
    Serializer برای نمایش جزئیات کامل سبد خرید، شامل تمام آیتم‌ها.
    مناسب برای درخواست‌های GET جهت نمایش سبد خرید کاربر.
    """
    # نمایش لیست آیتم‌های سبد با استفاده از CartItemSerializer
    items = CartItemSerializer(many=True, read_only=True)

    # تعداد ردیف‌های منحصر به فرد آیتم در سبد (مثلاً اگر 3 بار یک محصول را اضافه کنیم، این 3 حساب می‌شود)
    total_items_count = serializers.SerializerMethodField(read_only=True)

    # مجموع تعداد کل محصولات در سبد (جمع quantities تمام آیتم‌ها)
    total_quantity = serializers.SerializerMethodField(read_only=True)

    # جمع کل قیمت تمام آیتم‌ها در سبد (با استفاده از property 'total_price' هر آیتم)
    total_cart_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id',
            'user',             # ارتباط با کاربر (برای کاربران لاگین شده)
            'session_id',       # شناسه سشن (برای کاربران مهمان)
            'is_active',
            'total_items_count',# تعداد ردیف‌های آیتم
            'total_quantity',   # مجموع تعداد کل محصولات
            'total_cart_price', # جمع کل قیمت سبد
            'items',            # لیست تو در تو از آیتم‌های سبد
            'created_at',
            'updated_at',
        ]
        # فیلدهایی که نباید توسط کلاینت قابل تغییر باشند (برای عملیات GET)
        read_only_fields = [
            'id',
            'user',
            'session_id',
            'is_active',
            'total_items_count',
            'total_quantity',
            'total_cart_price',
            'items',
            'created_at',
            'updated_at',
        ]

    def get_total_items_count(self, obj: Cart):
        """محاسبه تعداد ردیف‌های آیتم منحصر به فرد در سبد."""
        return obj.items.count()

    def get_total_quantity(self, obj: Cart):
        """محاسبه مجموع تعداد تمام آیتم‌ها در سبد."""
        # استفاده از aggregate برای محاسبه جمع بهینه‌تر از loop زدن
        return obj.items.aggregate(total_q=Sum('quantity')).get('total_q', 0) or 0

    def get_total_cart_price(self, obj: Cart):
        """محاسبه جمع کل قیمت تمام آیتم‌ها در سبد."""
        # استفاده از aggregate برای محاسبه جمع بهینه‌تر از loop زدن
        return obj.items.aggregate(total_p=Sum('total_price')).get('total_p', 0) or 0


# -----------------------------------------------------------------------------
# Serializers برای نوشتن داده‌ها (تغییر سبد خرید)
# -----------------------------------------------------------------------------

class ProductAttributeValueForCartSerializer(serializers.PrimaryKeyRelatedField):
    """
    PrimaryKeyRelatedField سفارشی برای اطمینان از تعلق ویژگی‌ها به محصول مورد نظر.
    این کلاس در AddToCartSerializer برای فیلد attribute_values استفاده می‌شود.
    """
    def __init__(self, **kwargs):
        # Queryset اولیه خالی است و در متد validate_product_id در AddToCartSerializer تنظیم می‌شود
        # تا اطمینان حاصل شود که فقط ProductAttributeValue های مربوط به همان Product انتخاب شوند.
        super().__init__(queryset=ProductAttributeValue.objects.none(), **kwargs)


class AddToCartSerializer(serializers.Serializer):
    """
    Serializer برای افزودن محصول به سبد خرید.
    داده‌های ورودی: product_id, quantity, attribute_values (اختیاری).
    """
    product_id = serializers.IntegerField(required=True, help_text="شناسه محصول.")
    quantity = serializers.IntegerField(min_value=1, default=1, help_text="تعداد محصول (حداقل ۱).")
    attribute_values = ProductAttributeValueForCartSerializer(
        many=True,
        required=False,
        allow_empty=True,
        help_text="لیست شناسه‌های ProductAttributeValue انتخاب شده (مثلاً برای رنگ، سایز)."
    )

    # فیلدهای زیر برای استفاده در view یا model (پس از اعتبارسنجی) تنظیم می‌شوند
    # unit_price و product_name_snapshot برای snapshot کردن قیمت و نام محصول در لحظه افزودن
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    product_name_snapshot = serializers.CharField(max_length=255, read_only=True)

    def validate_product_id(self, value: int):
        """
        اعتبارسنجی Product ID و تنظیم Queryset مناسب برای ProductAttributeValue.
        همچنین Product را برای استفاده در متد validate اصلی، در context ذخیره می‌کند.
        """
        try:
            # یافتن محصول بر اساس ID
            product = Product.objects.get(id=value)
            # ذخیره محصول در context تا در متد validate اصلی قابل دسترسی باشد
            self.context['product'] = product
            # تنظیم queryset برای فیلد attribute_values تا فقط ProductAttributeValue های مرتبط با این محصول انتخاب شوند
            self.fields['attribute_values'].queryset = ProductAttributeValue.objects.filter(product=product)
            return value
        except Product.DoesNotExist:
            # اگر محصول یافت نشد، خطا نمایش داده می‌شود
            raise serializers.ValidationError(_("محصول با شناسه %(product_id)s یافت نشد.") % {'product_id': value})

    def validate(self, attrs: dict):
        """
        اعتبارسنجی نهایی داده‌ها و آماده‌سازی آن‌ها برای اضافه شدن به سبد خرید.
        در این متد، قیمت واحد (unit_price) و نام محصول (product_name_snapshot) snapshot می‌شوند.
        """
        product: Product = self.context['product'] # محصولی که در validate_product_id پیدا شد

        # تعیین قیمت واحد (unit_price): ابتدا قیمت تخفیف‌دار را بررسی می‌کنیم، اگر وجود داشت آن را استفاده می‌کنیم، در غیر این صورت قیمت اصلی.
        if product.discount_price is not None and product.discount_price > 0:
            attrs['unit_price'] = product.discount_price
        else:
            attrs['unit_price'] = product.price

        # ذخیره نام محصول در لحظه اضافه شدن به سبد (snapshot)
        attrs['product_name_snapshot'] = product.name

        # اگر attribute_values انتخاب شده باشد، آن‌ها را نیز در attrs ذخیره می‌کنیم تا در View قابل دسترسی باشند
        # (توجه: PrimaryKeyRelatedField در اینجا آبجکت‌ها را به جای ID برمی‌گرداند)
        if 'attribute_values' in attrs:
            attrs['attribute_values_objects'] = attrs['attribute_values']

        return attrs


class UpdateCartItemSerializer(serializers.ModelSerializer):
    """
    Serializer برای به‌روزرسانی تعداد (quantity) یک آیتم موجود در سبد خرید.
    این serializer فقط فیلد quantity را قابل تغییر می‌داند.
    """
    quantity = serializers.IntegerField(
        min_value=1,
        max_value=1000, # محدودیت حداکثر تعداد برای جلوگیری از مقادیر نامعتبر
        help_text="تعداد جدید محصول (بین ۱ تا ۱۰۰۰)."
    )

    class Meta:
        model = CartItem
        # فقط فیلد quantity قابل آپدیت است
        fields = ['quantity']
        # اطمینان از اینکه بقیه فیلدها از طریق این serializer قابل تغییر نباشند
        extra_kwargs = {
            'product': {'read_only': True},
            'cart': {'read_only': True},
            'unit_price': {'read_only': True}, # unit_price نباید تغییر کند، چون snapshot است
            'product_name_snapshot': {'read_only': True},
            'item_attributes': {'read_only': True}, # ویژگی‌ها پس از ایجاد قابل تغییر نیستند
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def update(self, instance: CartItem, validated_data: dict):
        """
        منطق به‌روزرسانی تعداد آیتم در سبد خرید.
        پس از تغییر quantity، قیمت کل (line_total) به طور خودکار توسط property 'total_price' محاسبه می‌شود.
        """
        new_quantity = validated_data.get('quantity', instance.quantity)

        # به‌روزرسانی تعداد
        instance.quantity = new_quantity
        # ذخیره تغییرات در دیتابیس
        instance.save()
        # توجه: نیازی به محاسبه مجدد total_price نیست، زیرا این یک property است و با خواندن instance دوباره محاسبه می‌شود.

        return instance
