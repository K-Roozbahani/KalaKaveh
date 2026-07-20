from home.handlers.base import BaseSectionHandler
from home.selectors import get_home_section_products


class CustomProductsHandler(BaseSectionHandler):

    def get_items(self, *, section):
        return get_home_section_products(section=section)