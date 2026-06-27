from rest_framework import serializers

from products.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    نمایش نظرات کاربران
    """

    user = serializers.StringRelatedField()

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