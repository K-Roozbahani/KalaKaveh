# home/constants.py

from django.db import models
from django.utils.translation import gettext_lazy as _


class HomeSectionType(models.TextChoices):
    """
    انواع سکشن‌های صفحه اصلی
    """

    HERO_SLIDER = "hero_slider", _("اسلایدر اصلی")

    BANNER = "banner", _("بنر")

    CATEGORIES = "categories", _("دسته‌بندی‌ها")

    FEATURED_PRODUCTS = "featured_products", _("محصولات ویژه")

    LATEST_PRODUCTS = "latest_products", _("جدیدترین محصولات")

    BEST_SELLER_PRODUCTS = "best_seller_products", _("پرفروش‌ترین محصولات")

    DISCOUNT_PRODUCTS = "discount_products", _("محصولات تخفیف‌دار")

    BRANDS = "brands", _("برندها")

    CUSTOM_PRODUCTS = "custom_products", _("محصولات انتخابی")



class HomeSectionLayout(models.TextChoices):
    GRID = "grid", _("شبکه‌ای")
    SLIDER = "slider", _("اسلایدر")
    CAROUSEL = "carousel", _("کاروسل")
    BANNER = "banner", _("بنر")