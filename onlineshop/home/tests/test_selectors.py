from django.test import TestCase

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
from home.selectors import (
    get_active_banners,
    get_active_hero_slides,
    get_active_home_sections,
    get_home_section_brands,
    get_home_section_categories,
    get_home_section_products,
)


class GetActiveHomeSectionsTests(TestCase):

    def test_returns_only_active_sections(self):
        active = create_featured_product_section(
            is_active=True,
        )

        create_featured_product_section(
            is_active=False,
        )

        queryset = get_active_home_sections()

        self.assertEqual(
            list(queryset),
            [active],
        )

    def test_orders_sections(self):
        second = create_featured_product_section(
            order=2,
        )

        first = create_featured_product_section(
            order=1,
        )

        queryset = get_active_home_sections()

        self.assertEqual(
            list(queryset),
            [first, second],
        )

class GetActiveHeroSlidesTests(TestCase):

    def test_returns_only_section_items(self):
        section = create_hero_section()

        create_hero_slide(
            section=section,
        )

        other = create_hero_section()

        create_hero_slide(
            section=other,
        )

        queryset = get_active_hero_slides(
            section=section,
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

    def test_returns_only_active_items(self):
        section = create_hero_section()

        active = create_hero_slide(
            section=section,
            is_active=True,
        )

        create_hero_slide(
            section=section,
            is_active=False,
        )

        queryset = get_active_hero_slides(
            section=section,
        )

        self.assertEqual(
            list(queryset),
            [active],
        )

    def test_orders_items(self):
        section = create_hero_section()

        second = create_hero_slide(
            section=section,
            order=2,
        )

        first = create_hero_slide(
            section=section,
            order=1,
        )

        queryset = get_active_hero_slides(
            section=section,
        )

        self.assertEqual(
            list(queryset),
            [first, second],
        )


class GetActiveHeroSlidesTests(TestCase):

    def test_returns_only_section_items(self):
        section = create_hero_section()

        create_hero_slide(
            section=section,
        )

        other = create_hero_section()

        create_hero_slide(
            section=other,
        )

        queryset = get_active_hero_slides(
            section=section,
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

    def test_returns_only_active_items(self):
        section = create_hero_section()

        active = create_hero_slide(
            section=section,
            is_active=True,
        )

        create_hero_slide(
            section=section,
            is_active=False,
        )

        queryset = get_active_hero_slides(
            section=section,
        )

        self.assertEqual(
            list(queryset),
            [active],
        )

    def test_orders_items(self):
        section = create_hero_section()

        second = create_hero_slide(
            section=section,
            order=2,
        )

        first = create_hero_slide(
            section=section,
            order=1,
        )

        queryset = get_active_hero_slides(
            section=section,
        )

        self.assertEqual(
            list(queryset),
            [first, second],
        )

    def test_orders_items(self):
        """
        اسلایدها بر اساس ترتیب نمایش مرتب شوند.
        """

        section = create_hero_section()

        second = create_hero_slide(
            section=section,
            order=2,
        )

        first = create_hero_slide(
            section=section,
            order=1,
        )

        queryset = get_active_hero_slides(
            section=section,
        )

        self.assertEqual(
            list(queryset),
            [first, second],
        )


class GetActiveBannersTests(TestCase):

    def test_returns_only_section_items(self):
        section = create_banner_section()

        create_banner(section=section)

        other = create_banner_section()

        create_banner(section=other)

        queryset = get_active_banners(
            section=section,
        )

        self.assertEqual(
            queryset.count(),
            1,
        )

    def test_returns_only_active_items(self):
        section = create_banner_section()

        active = create_banner(
            section=section,
        )

        create_banner(
            section=section,
            is_active=False,
        )

        queryset = get_active_banners(
            section=section,
        )

        self.assertEqual(
            list(queryset),
            [active],
        )

    def test_orders_items(self):
        """
        بنرها بر اساس ترتیب نمایش مرتب شوند.
        """

        section = create_banner_section()

        second = create_banner(
            section=section,
            order=2,
        )

        first = create_banner(
            section=section,
            order=1,
        )

        queryset = get_active_banners(
            section=section,
        )

        self.assertEqual(
            list(queryset),
            [first, second],
        )


class GetHomeSectionProductsTests(TestCase):

    def test_returns_products_for_section(self):
        section = create_featured_product_section()

        item = create_home_section_product(
            section=section,
        )

        create_home_section_product()

        queryset = get_home_section_products(
            section=section,
        )

        self.assertEqual(
            list(queryset),
            [item],
        )

    def test_orders_products(self):
        """
        محصولات بر اساس ترتیب نمایش مرتب شوند.
        """

        section = create_featured_product_section()

        second = create_home_section_product(
            section=section,
            order=2,
        )

        first = create_home_section_product(
            section=section,
            order=1,
        )

        queryset = get_home_section_products(
            section=section,
        )

        self.assertEqual(
            list(queryset),
            [first, second],
        )


class GetHomeSectionCategoriesTests(TestCase):

    def test_returns_categories_for_section(self):
        section = create_category_section()

        item = create_home_section_category(
            section=section,
        )

        create_home_section_category()

        queryset = get_home_section_categories(
            section=section,
        )

        self.assertEqual(
            list(queryset),
            [item],
        )

    def test_orders_categories(self):
        """
        دسته‌بندی‌ها بر اساس ترتیب نمایش مرتب شوند.
        """

        section = create_category_section()

        second = create_home_section_category(
            section=section,
            order=2,
        )

        first = create_home_section_category(
            section=section,
            order=1,
        )

        queryset = get_home_section_categories(
            section=section,
        )

        self.assertEqual(
            list(queryset),
            [first, second],
        )


class GetHomeSectionBrandsTests(TestCase):

    def test_returns_brands_for_section(self):
        section = create_brand_section()

        item = create_home_section_brand(
            section=section,
        )

        create_home_section_brand()

        queryset = get_home_section_brands(
            section=section,
        )

        self.assertEqual(
            list(queryset),
            [item],
        )

    def test_orders_brands(self):
        """
        برندها بر اساس ترتیب نمایش مرتب شوند.
        """

        section = create_brand_section()

        second = create_home_section_brand(
            section=section,
            order=2,
        )

        first = create_home_section_brand(
            section=section,
            order=1,
        )

        queryset = get_home_section_brands(
            section=section,
        )

        self.assertEqual(
            list(queryset),
            [first, second],
        )


