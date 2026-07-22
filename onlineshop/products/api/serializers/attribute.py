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
            'descriptions'
        )


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    """"
    مقدار ویژگیهای تنوع محصول
    """

    Attribute = ProductAttributeSerializer(read_only=True)

    class Meta:
        fields = (
            'id',
            'attribute',
            'value',
        )


class VariantAttributeSerializer(serializers.ModelSerializer):
    """"
        مدل واسط بین تنوع محصول و مقدار ویژگی
    """

    attribute = ProductAttributeSerializer(read_only=True)

    class Meta:
        fields = (
            'id',
            'attribute',
            'value',
        )