from rest_framework import serializers

from products.models import Brand


class BrandSerializer(serializers.ModelSerializer):
    """
    نمایش اطلاعات برند
    """

    class Meta:
        model = Brand

        fields = (
            "id",
            "name",
            "slug",
            "logo",
        )

        read_only_fields = fields