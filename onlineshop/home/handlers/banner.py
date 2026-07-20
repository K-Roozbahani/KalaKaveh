from home.handlers.base import BaseSectionHandler
from home.selectors import get_active_banners


class BannerHandler(BaseSectionHandler):

    def get_items(self, *, section):
        return get_active_banners(section=section)