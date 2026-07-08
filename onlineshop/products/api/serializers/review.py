from rest_framework import serializers

from products.models import Review


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

        if not 1 <= value <= 5:
            raise serializers.ValidationError(
                "امتیاز باید بین ۱ تا ۵ باشد."
            )

        return value