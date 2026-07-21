from django.test import TestCase

from home.services import get_home_sections
from home.tests.factories import (
    create_featured_product_section,
    create_home_section_product,
    create_home_section_brand,
    create_brand_section
)
from products.tests.factories import (
    create_product,
    create_variant,
)


class GetHomeSectionsTests(TestCase):

    def test_returns_sections_with_items(self):
        section = create_featured_product_section()

        product = create_product()
        create_variant(product=product)

        create_home_section_product(
            section=section,
            product=product,
        )

        result = get_home_sections()

        self.assertEqual(len(result), 1)

        self.assertEqual(
            result[0]["section"],
            section,
        )

        self.assertEqual(
            list(result[0]["items"]),
            [product],
        )

    def test_returns_empty_list(self):
        result = get_home_sections()

        self.assertEqual(
            result,
            [],
        )

    def test_returns_multiple_sections(self):
        first = create_featured_product_section()
        second = create_brand_section()

        product = create_product()
        create_variant(product=product)

        create_home_section_product(
            section=first,
            product=product,
        )

        create_home_section_brand(
            section=second,
        )

        result = get_home_sections()

        self.assertEqual(
            len(result),
            2,
        )