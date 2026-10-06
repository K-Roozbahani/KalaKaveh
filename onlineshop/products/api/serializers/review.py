from phonenumbers.phonenumberutil import is_mobile_number_portable_region
from rest_framework import serializers

from products.models import Review
from products.validators import (
    validate_review_comment,
    validate_review_rating,
)


class ReviewSummarySerializer(serializers.Serializer):
    """
    خلاصه امتیازهای محصول
    """

    average_rate = serializers.FloatField()
    total_count = serializers.IntegerField()
    counts = serializers.DictField()


class ReviewSerializer(serializers.ModelSerializer):
    """
    نمایش نظرات کاربران
    """

    user = serializers.CharField(
        source="user.get_full_name",
        read_only=True,
    )

    class Meta:
        model = Review

        fields = (
            "id",
            "user",
            "rating",
            "comment",
            "created_at",
        )

        read_only_fields = fields


class ReviewWriteSerializer(serializers.ModelSerializer):
    """
    ثبت و ویرایش نظر
    """

    class Meta:
        model = Review
        fields = (
            "rating",
            "comment",
        )

    def validate_rating(self, value):
        """
        اعتبارسنجی امتیاز
        """

        validate_review_rating(
            rating=value,
        )

        return value

    def validate_comment(self, value):
        """
        اعتبارسنجی و پاکسازی متن نظر
        """

        return validate_review_comment(
            comment=value,
        )


class UserReviewsSerializer(serializers.ModelSerializer):
    """
    نمایش نظرات کاربر جاری
    """

    product = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = (
            "id",
            "status",
            "user",
            "product",
            "rating",
            "comment",
            "created_at",
        )

        read_only_fields = (
            "id",
            "user",
            "product",
            "status",
            "created_at",
        )

    def get_product(self, obj):
        """
        دریافت اطلاعات محصول مربوط به نظر
        """

        product = obj.product

        variant = product.variants.first()
        image = product.images.first()

        request = self.context.get("request")

        return {
            "id": product.id,
            "name": product.name,
            "slug": product.slug,
            "brand": product.brand.name if product.brand else None,
            "category": product.category.name if product.category else None,
            "price": variant.price if variant else None,
            "discount_amount": variant.discount_amount if variant else None,
            "final_price": variant.final_price if variant else None,
            "image": (
                request.build_absolute_uri(image.image.url)
                if image and request
                else image.url if image else None
            ),
        }

    def get_status(self, obj):
        """
        انمایش وضعیت نظر
        """
        if obj.is_valid:
            return "معتبر"
        else:
            return "در انتظار تایید"