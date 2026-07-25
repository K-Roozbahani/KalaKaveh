from rest_framework import serializers


from products.models import (ProductAttribute,
                             ProductVariantAttribute,
                             ProductAttributeValue,
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
    """"
    مقدار ویژگیهای تنوع محصول
    """

    attribute = ProductAttributeSerializer(read_only=True)

    class Meta:
        model = ProductAttributeValue

        fields = (
            'id',
            'attribute',
            'value',
        )


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