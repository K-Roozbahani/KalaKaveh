from rest_framework import serializers
from products.modesl import (
    Category, Brand, ProductAttribute, Product,
    ProductAttributeValue, ProductImage, Review
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


# --- 5. Product Serializers (The Core) ---

class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user_name', 'comment', 'rating', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    # فیلدهای خواندنی (Read-only) برای نمایش اطلاعات کامل در GET
    category_name = serializers.ReadOnlyField(source='category.name')
    brand_name = serializers.ReadOnlyField(source='brand.name')
    images = ProductImageSerializer(many=True, read_only=True)
    attribute_values = ProductAttributeValueSerializer(many=True, read_only=True)
    reviews = ProductReviewSerializer(many=True, read_only=True)

    # محاسبه میانگین امتیازات به صورت خودکار
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'discount_price',
            'stock', 'category', 'category_name', 'brand', 'brand_name',
            'main_image', 'images', 'attributes', 'attribute_values',
            'reviews', 'average_rating', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']

    def get_average_rating(self, obj):
        # محاسبه میانگین امتیاز از طریق Relation
        reviews = obj.reviews.all()
        if reviews.exists():
            return reviews.aggregate(serializers.Avg('rating'))['rating__avg']
        return 0


# --- 6. Review Serializer (For creating reviews) ---

class ReviewCreateSerializer(serializers.ModelSerializer):
    """
    سریالایزر مخصوص زمانی که کاربر می‌خواهد نظر ثبت کند
    """

    class Meta:
        model = Review
        fields = ['id', 'comment', 'rating', 'created_at']


# --- 7. Extra: Specialized Product Serializer for Writing ---

class ProductWriteSerializer(serializers.ModelSerializer):
    """
    اگر نیاز دارید هنگام ساخت محصول، مقادیر ویژگی‌ها (AttributeValues) را هم همزمان بفرستید
    """

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['slug']
