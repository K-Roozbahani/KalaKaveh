from django.test import TestCase

from home.constants import HomeSectionType
from home.services import get_home_sections
from home.tests.factories import (
    create_brand_section,
    create_featured_product_section,
    create_home_section_brand,
    create_home_section_product,
)
from products.tests.factories import (
    create_product,
    create_variant,
)


class GetHomeSectionsTests(TestCase):

    def test_returns_grouped_sections(self):
        section = create_featured_product_section()

        product = create_product()
        create_variant(product=product)

        create_home_section_product(
            section=section,
            product=product,
        )

        result = get_home_sections()

        self.assertIn(
            HomeSectionType.FEATURED_PRODUCTS,
            result,
        )

        self.assertEqual(
            len(result[HomeSectionType.FEATURED_PRODUCTS]),
            1,
        )

        self.assertEqual(
            result[HomeSectionType.FEATURED_PRODUCTS][0]["section"],
            section,
        )

        self.assertEqual(
            list(
                result[HomeSectionType.FEATURED_PRODUCTS][0]["items"],
            ),
            [product],
        )

    def test_returns_empty_dict(self):
        result = get_home_sections()

        self.assertEqual(
            result,
            {},
        )

    def test_groups_multiple_section_types(self):
        featured = create_featured_product_section()
        brands = create_brand_section()

        product = create_product()
        create_variant(product=product)

        create_home_section_product(
            section=featured,
            product=product,
        )

        create_home_section_brand(
            section=brands,
        )

        result = get_home_sections()

        self.assertIn(
            HomeSectionType.FEATURED_PRODUCTS,
            result,
        )

        self.assertIn(
            HomeSectionType.BRANDS,
            result,
        )

        self.assertEqual(
            len(result),
            2,
        )

        self.assertEqual(
            len(result[HomeSectionType.FEATURED_PRODUCTS]),
            1,
        )

        self.assertEqual(
            len(result[HomeSectionType.BRANDS]),
            1,
        )