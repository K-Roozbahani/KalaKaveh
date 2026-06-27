from rest_framework import serializers

from products.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    نمایش اطلاعات دسته‌بندی
    """

    class Meta:
        model = Category

        fields = (
            "id",
            "name",
            "slug",
        )

        read_only_fields = fields