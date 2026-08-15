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