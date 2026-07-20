from rest_framework import serializers

from home.constants import HomeSectionType
from home.models import Banner, HeroSlide

from products.api.serializers import (
    ProductListSerializer,
    BrandSerializer,
    CategorySerializer
)


class HeroSlideSerializer(serializers.ModelSerializer):

    class Meta:
        model = HeroSlide
        fields = (
            "id",
            "title",
            "subtitle",
            "desktop_image",
            "mobile_image",
            "button_text",
            "button_url",
        )


class BannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = (
            "id",
            "title",
            "desktop_image",
            "mobile_image",
            "url",
        )


class HomeSectionSerializer(serializers.Serializer):

    title = serializers.CharField(
        source="section.title",
    )

    section_type = serializers.CharField(
        source="section.section_type",
    )

    layout = serializers.CharField(
        source="section.layout",
    )

    items = serializers.SerializerMethodField()

    def get_items(self, obj):

        section = obj["section"]

        items = obj["items"]

        match section.section_type:

            case HomeSectionType.HERO_SLIDER:
                return HeroSlideSerializer(
                    items,
                    many=True,
                    context=self.context,
                ).data

            case HomeSectionType.BANNER:
                return BannerSerializer(
                    items,
                    many=True,
                    context=self.context,
                ).data

            case HomeSectionType.CATEGORIES:
                return CategorySerializer(
                    [item.category for item in items],
                    many=True,
                    context=self.context,
                ).data

            case HomeSectionType.BRANDS:
                return BrandSerializer(
                    [item.brand for item in items],
                    many=True,
                    context=self.context,
                ).data

            case _:
                return ProductListSerializer(
                    items,
                    many=True,
                    context=self.context,
                ).data