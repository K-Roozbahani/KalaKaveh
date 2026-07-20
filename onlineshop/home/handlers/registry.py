from home.constants import HomeSectionType

from home.handlers.banner import BannerHandler
from home.handlers.base import BaseSectionHandler
from home.handlers.brands import BrandHandler
from home.handlers.categories import CategoryHandler
from home.handlers.hero_slider import HeroSliderHandler
from home.handlers.product import ProductSectionHandler


SECTION_HANDLERS: dict[str, BaseSectionHandler] = {
    HomeSectionType.HERO_SLIDER: HeroSliderHandler(),
    HomeSectionType.BANNER: BannerHandler(),
    HomeSectionType.CATEGORIES: CategoryHandler(),
    HomeSectionType.BRANDS: BrandHandler(),

    # سکشن‌های محصولات
    HomeSectionType.FEATURED_PRODUCTS: ProductSectionHandler(),
    HomeSectionType.LATEST_PRODUCTS: ProductSectionHandler(),
    HomeSectionType.BEST_SELLER_PRODUCTS: ProductSectionHandler(),
    HomeSectionType.DISCOUNT_PRODUCTS: ProductSectionHandler(),
    HomeSectionType.CUSTOM_PRODUCTS: ProductSectionHandler(),
}


def get_section_handler(
    *,
    section_type: str,
) -> BaseSectionHandler:
    """
    دریافت Handler مربوط به نوع سکشن.
    """

    try:
        return SECTION_HANDLERS[section_type]
    except KeyError as exc:
        raise ValueError(
            f"Unsupported home section type: {section_type}"
        ) from exc