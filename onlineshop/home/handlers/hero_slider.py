from home.handlers.base import BaseSectionHandler
from home.selectors import get_active_hero_slides


class HeroSliderHandler(BaseSectionHandler):

    def get_items(self, *, section):
        return get_active_hero_slides(section=section)