from rest_framework import serializers

from home.constants import HomeSectionType
from home.models import Banner, HeroSlide

from products.api.serializers import (
    BrandSerializer,
    CategorySerializer,
    ProductListSerializer,
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
    """
    Serializer مربوط به هر سکشن صفحه اصلی.
    """

    SECTION_SERIALIZERS = {
        HomeSectionType.HERO_SLIDER: HeroSlideSerializer,
        HomeSectionType.BANNER: BannerSerializer,
    }

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
        """
        سریالایز آیتم‌های هر سکشن.
        """

        section = obj["section"]
        items = obj["items"]

        serializer_class = self.SECTION_SERIALIZERS.get(
            section.section_type,
        )

        if serializer_class is not None:
            return serializer_class(
                items,
                many=True,
                context=self.context,
            ).data

        if section.section_type == HomeSectionType.CATEGORIES:
            return CategorySerializer(
                [item.category for item in items],
                many=True,
                context=self.context,
            ).data

        if section.section_type == HomeSectionType.BRANDS:
            return BrandSerializer(
                [item.brand for item in items],
                many=True,
                context=self.context,
            ).data

        return ProductListSerializer(
            items,
            many=True,
            context=self.context,
        ).data

class HomePageSerializer(serializers.Serializer):
    """
    Serializer خروجی صفحه اصلی.
    """

    def to_representation(self, instance):

        data = {}

        for section_type, sections in instance.items():

            data[section_type] = HomeSectionSerializer(
                sections,
                many=True,
                context=self.context,
            ).data

        return data