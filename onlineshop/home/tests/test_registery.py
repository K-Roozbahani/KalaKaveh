from django.test import TestCase

from home.constants import HomeSectionType
from home.handlers.banner import BannerHandler
from home.handlers.brands import BrandHandler
from home.handlers.categories import CategoryHandler
from home.handlers.hero_slider import HeroSliderHandler
from home.handlers.product import ProductSectionHandler
from home.handlers.registry import get_section_handler


class GetSectionHandlerTests(TestCase):

    def test_returns_hero_slider_handler(self):
        handler = get_section_handler(
            section_type=HomeSectionType.HERO_SLIDER,
        )

        self.assertIsInstance(
            handler,
            HeroSliderHandler,
        )

    def test_returns_banner_handler(self):
        handler = get_section_handler(
            section_type=HomeSectionType.BANNER,
        )

        self.assertIsInstance(
            handler,
            BannerHandler,
        )

    def test_returns_category_handler(self):
        handler = get_section_handler(
            section_type=HomeSectionType.CATEGORIES,
        )

        self.assertIsInstance(
            handler,
            CategoryHandler,
        )

    def test_returns_brand_handler(self):
        handler = get_section_handler(
            section_type=HomeSectionType.BRANDS,
        )

        self.assertIsInstance(
            handler,
            BrandHandler,
        )

    def test_returns_product_handler_for_featured_products(self):
        handler = get_section_handler(
            section_type=HomeSectionType.FEATURED_PRODUCTS,
        )

        self.assertIsInstance(
            handler,
            ProductSectionHandler,
        )

    def test_returns_product_handler_for_latest_products(self):
        handler = get_section_handler(
            section_type=HomeSectionType.LATEST_PRODUCTS,
        )

        self.assertIsInstance(
            handler,
            ProductSectionHandler,
        )

    def test_returns_product_handler_for_best_seller_products(self):
        handler = get_section_handler(
            section_type=HomeSectionType.BEST_SELLER_PRODUCTS,
        )

        self.assertIsInstance(
            handler,
            ProductSectionHandler,
        )

    def test_returns_product_handler_for_discount_products(self):
        handler = get_section_handler(
            section_type=HomeSectionType.DISCOUNT_PRODUCTS,
        )

        self.assertIsInstance(
            handler,
            ProductSectionHandler,
        )

    def test_returns_product_handler_for_custom_products(self):
        handler = get_section_handler(
            section_type=HomeSectionType.CUSTOM_PRODUCTS,
        )

        self.assertIsInstance(
            handler,
            ProductSectionHandler,
        )

    def test_raises_error_for_unknown_section_type(self):
        with self.assertRaises(ValueError):
            get_section_handler(
                section_type="invalid",
            )