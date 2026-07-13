from rest_framework import serializers

from products.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    نمایش اطلاعات دسته‌بندی
    """
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Category

        fields = (
            "id",
            "name",
            "slug",
            "parent",
        )

        read_only_fields = fields

    def get_parent(self, obj):
        if not obj.parent:
            return None

        return {
            "id": obj.parent.id,
            "name": obj.parent.name,
            "slug": obj.parent.slug,
            "parent": self.get_parent(obj.parent),
        }