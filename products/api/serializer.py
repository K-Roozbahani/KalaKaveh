from rest_framework import serializers
from products.models import (
    Category, Brand, ProductAttribute, Product,
    ProductAttributeValue, ProductImage, Review,
    VariantImage, ProductVariant, ProductVariantAttribute
)


# --- 1. Category Serializers ---

class CategorySerializer(serializers.ModelSerializer):
    # نمایش زیردسته‌ها به صورت بازگشتی (Recursive)
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'subcategories']
        read_only_fields = ['slug']

    def get_subcategories(self, obj):
        # برای جلوگیری از حلقه بی‌نهایت در دیتای خیلی عمیق،
        # اینجا فقط سطح اول را نمایش می‌دهیم یا می‌توانید از یک سریالایزر ساده‌تر استفاده کنید
        serializer = CategorySerializer(obj.subcategories.all(), many=True)
        return serializer.data


# --- 2. Brand Serializers ---

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug', 'logo']
        read_only_fields = ['slug']


# --- 3. Product Attribute Serializers ---

class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['id', 'name', 'description']


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    # نمایش نام ویژگی به جای فقط ID
    attribute_name = serializers.ReadOnlyField(source='attribute.name')

    class Meta:
        model = ProductAttributeValue
        fields = ['id', 'attribute', 'attribute_name', 'value']


# --- 4. Product Image Serializers ---

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text']

# --- 5. Variants serializer ---

class VariantImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = VariantImage
        fields = (
            "id",
            "image",
            "is_primary",
        )

class ProductVariantAttributeSerializer(
    serializers.ModelSerializer
):
    attribute = serializers.CharField(
        source="attribute_value.attribute.name",
        read_only=True
    )

    value = serializers.CharField(
        source="attribute_value.value",
        read_only=True
    )

    class Meta:
        model = ProductVariantAttribute
        fields = (
            "id",
            "attribute",
            "value",
        )

class ProductVariantSerializer(
        serializers.ModelSerializer
    ):
        attributes = ProductVariantAttributeSerializer(
            source="variant_attributes",
            many=True,
            read_only=True
        )

        images = VariantImageSerializer(
            many=True,
            read_only=True
        )

        class Meta:
            model = ProductVariant
            fields = (
                "id",
                "sku",
                "price",
                'discount_amount',
                'final_price',
                "stock",
                "is_active",
                "attributes",
                "images",
            )


class ProductVariantDetailSerializer(
    serializers.ModelSerializer
):

    images = VariantImageSerializer(
        many=True,
        read_only=True
    )

    attributes = ProductAttributeValueSerializer(
        source="attribute_values",
        many=True,
        read_only=True
    )

    discount_percent = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant

        fields = (
            "id",
            "sku",
            "price",
            "discount_amount",
            "discount_percent",
            "final_price",
            "stock",
            "images",
            "attributes",
        )

    def get_discount_percent(
        self,
        obj
    ):
        if obj.price == 0:
            return 0

        return round(
            (obj.discount_amount / obj.price) * 100
        )

# --- 5. Product Serializers (The Core) ---

class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'comment', 'rating', 'created_at']

class ProductListSerializer(
    serializers.ModelSerializer
):

    min_price = serializers.IntegerField(
        read_only=True
    )

    min_final_price = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "min_price",
            "min_final_price",
        )



class ProductDetailSerializer(serializers.ModelSerializer):
    # فیلدهای خواندنی (Read-only) برای نمایش اطلاعات کامل در GET
    category_name = serializers.ReadOnlyField(source='category.name')
    brand_name = serializers.ReadOnlyField(source='brand.name')
    images = ProductImageSerializer(many=True, read_only=True)
    attribute_values = ProductAttributeValueSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    reviews = ProductReviewSerializer(many=True, read_only=True)

    # محاسبه میانگین امتیازات به صورت خودکار
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description',
            'category_name', 'brand_name',
            'images', 'attribute_values',
            'reviews', 'average_rating',
            'is_active', 'variants'
        ]
        read_only_fields = '__all__'

# --- 6. Review Serializer (For creating reviews) ---

class ReviewCreateSerializer(serializers.ModelSerializer):
    """
    سریالایزر مخصوص زمانی که کاربر می‌خواهد نظر ثبت کند
    """

    class Meta:
        model = Review
        fields = ['id', 'comment', 'rating', 'created_at']


# --- 7. Extra: Specialized Product Serializer for Writing ---

class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """
    اگر نیاز دارید هنگام ساخت محصول، مقادیر ویژگی‌ها (AttributeValues) را هم همزمان بفرستید
    """

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['slug']
