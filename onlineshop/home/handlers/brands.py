from home.handlers.base import BaseSectionHandler
from home.selectors import get_home_section_brands


class BrandHandler(BaseSectionHandler):

    def get_items(self, *, section):
        return get_home_section_brands(section=section)