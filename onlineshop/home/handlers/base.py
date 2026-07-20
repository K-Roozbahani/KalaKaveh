from abc import ABC, abstractmethod

from home.models import HomeSection


class BaseSectionHandler(ABC):
    """
    کلاس پایه Handler های صفحه اصلی.
    """

    @abstractmethod
    def get_items(self, *, section: HomeSection):
        """
        دریافت آیتم‌های سکشن.
        """
        raise NotImplementedError