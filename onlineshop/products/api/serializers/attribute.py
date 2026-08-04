from rest_framework import serializers


from products.models import (ProductAttribute,
                             ProductVariantAttribute,
                             ProductAttributeValue, ProductAttributeValueProperty,
                             )


class ProductAttributeSerializer(serializers.ModelSerializer):
    """"
    ویژگیهای تنوع محصول
    """

    class Meta:
        model = ProductAttribute

        fields = (
            'id',
            'name',
            'description'
        )


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    """
    Serializer مقدار ویژگی محصول.
    """

    attribute = serializers.CharField(
        source="attribute.name",
        read_only=True,
    )

    properties = serializers.SerializerMethodField()

    class Meta:
        model = ProductAttributeValue

        fields = (
            "attribute",
            "value",
            "properties",
        )

    def get_properties(self, obj):
        """
        تبدیل Property های ویژگی به دیکشنری.

        خروجی:
            {
                "color_code": "#FF0000",
                "rgb": "255,0,0"
            }
        """

        return {
            item.key: item.value
            for item in obj.properties.all()
        }


class VariantAttributeSerializer(serializers.ModelSerializer):
    """"
        مدل واسط بین تنوع محصول و مقدار ویژگی
    """

    attribute_value = ProductAttributeValueSerializer(read_only=True)

    class Meta:
        model = ProductVariantAttribute

        fields = (
            'id',
            'attribute_value',
        )