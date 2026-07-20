"""
Selectorهای مربوط به صفحه اصلی فروشگاه
"""

from django.db.models import QuerySet

from home.models import (
    Banner,
    HeroSlide,
    HomeSection,
    HomeSectionBrand,
    HomeSectionCategory,
    HomeSectionProduct,
)


def get_active_home_sections() -> QuerySet[HomeSection]:
    """
    دریافت سکشن‌های فعال صفحه اصلی.
    """

    return (
        HomeSection.objects
        .filter(is_active=True)
        .order_by("order")
    )


def get_active_hero_slides(
    *,
    section: HomeSection,
) -> QuerySet[HeroSlide]:
    """
    دریافت اسلایدهای فعال سکشن.
    """

    return (
        HeroSlide.objects
        .filter(
            section=section,
            is_active=True,
        )
        .order_by("order")
    )


def get_active_banners(
    *,
    section: HomeSection,
) -> QuerySet[Banner]:
    """
    دریافت بنرهای فعال سکشن.
    """

    return (
        Banner.objects
        .filter(
            section=section,
            is_active=True,
        )
    )


def get_home_section_products(
    *,
    section: HomeSection,
) -> QuerySet[HomeSectionProduct]:
    """
    دریافت محصولات انتخابی سکشن.
    """

    return (
        HomeSectionProduct.objects
        .filter(section=section)
        .select_related(
            "product",
            "product__brand",
            "section",
        )
        .prefetch_related(
            "product__images",
            "product__variants",
        )
        .order_by("order")
    )


def get_home_section_categories(
    *,
    section: HomeSection,
) -> QuerySet[HomeSectionCategory]:
    """
    دریافت دسته‌بندی‌های انتخابی سکشن.
    """

    return (
        HomeSectionCategory.objects
        .filter(section=section)
        .select_related(
            "category",
            "category__parent",
            "section",
        )
        .order_by("order")
    )


def get_home_section_brands(
    *,
    section: HomeSection,
) -> QuerySet[HomeSectionBrand]:
    """
    دریافت برندهای انتخابی سکشن.
    """

    return (
        HomeSectionBrand.objects
        .filter(section=section)
        .select_related(
            "brand",
            "section",
        )
        .order_by("order")
    )