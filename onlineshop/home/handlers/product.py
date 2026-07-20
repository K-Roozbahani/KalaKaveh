from home.handlers.base import BaseSectionHandler
from home.models import HomeSection

from products.selectors import get_home_products


class ProductSectionHandler(BaseSectionHandler):
    """
    Handler مربوط به سکشن‌های محصولات صفحه اصلی.
    """

    def get_items(
        self,
        *,
        section: HomeSection,
    ):
        """
        دریافت محصولات سکشن.
        """

        return get_home_products(
            section_type=section.section_type,
            limit=section.config.get("limit", 8),
        )