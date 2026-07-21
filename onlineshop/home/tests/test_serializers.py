from django.test import TestCase

from home.api.serializers import HomeSectionSerializer
from home.tests.factories import (
    create_banner,
    create_banner_section,
    create_brand_section,
    create_category_section,
    create_featured_product_section,
    create_hero_section,
    create_hero_slide,
    create_home_section_brand,
    create_home_section_category,
    create_home_section_product,
)
from products.tests.factories import (
    create_brand,
    create_category,
    create_product,
    create_variant,
)


class HomeSectionSerializerTests(TestCase):

    def test_serializes_hero_section(self):
        section = create_hero_section()

        slide = create_hero_slide(
            section=section,
        )

        serializer = HomeSectionSerializer(
            [
                {
                    "section": section,
                    "items": [slide],
                }
            ],
            many=True,
        )

        data = serializer.data[0]

        self.assertEqual(
            data["title"],
            section.title,
        )

        self.assertEqual(
            data["section_type"],
            section.section_type,
        )

        self.assertEqual(
            len(data["items"]),
            1,
        )


    def test_serializes_banner_section(self):
        section = create_banner_section()

        banner = create_banner(
            section=section,
        )

        serializer = HomeSectionSerializer(
            [
                {
                    "section": section,
                    "items": [banner],
                }
            ],
            many=True,
        )

        self.assertEqual(
            len(serializer.data[0]["items"]),
            1,
        )



    def test_serializes_category_section(self):
        section = create_category_section()

        category = create_category()

        item = create_home_section_category(
            section=section,
            category=category,
        )

        serializer = HomeSectionSerializer(
            [
                {
                    "section": section,
                    "items": [item],
                }
            ],
            many=True,
        )

        self.assertEqual(
            serializer.data[0]["items"][0]["id"],
            category.id,
        )


    def test_serializes_brand_section(self):
        section = create_brand_section()

        brand = create_brand()

        item = create_home_section_brand(
            section=section,
            brand=brand,
        )

        serializer = HomeSectionSerializer(
            [
                {
                    "section": section,
                    "items": [item],
                }
            ],
            many=True,
        )

        self.assertEqual(
            serializer.data[0]["items"][0]["id"],
            brand.id,
        )


    def test_serializes_product_section(self):
        section = create_featured_product_section()

        product = create_product()

        create_variant(
            product=product,
        )

        serializer = HomeSectionSerializer(
            [
                {
                    "section": section,
                    "items": [product],
                }
            ],
            many=True,
        )

        self.assertEqual(
            serializer.data[0]["items"][0]["id"],
            product.id,
        )


    def test_contains_common_fields(self):
        section = create_featured_product_section()

        serializer = HomeSectionSerializer(
            [
                {
                    "section": section,
                    "items": [],
                }
            ],
            many=True,
        )

        data = serializer.data[0]

        self.assertIn("title", data)
        self.assertIn("section_type", data)
        self.assertIn("layout", data)
        self.assertIn("items", data)