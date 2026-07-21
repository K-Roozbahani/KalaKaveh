from home.constants import (
    HomeSectionLayout,
    HomeSectionType,
)
from home.models import (
    Banner,
    HeroSlide,
    HomeSection,
    HomeSectionBrand,
    HomeSectionCategory,
    HomeSectionProduct,
)

from products.tests.factories import (
    create_brand,
    create_category,
    create_product,
)


def create_home_section(**kwargs):
    return HomeSection.objects.create(
        title=kwargs.get(
            "title",
            "سکشن تست",
        ),
        section_type=kwargs.get(
            "section_type",
            HomeSectionType.FEATURED_PRODUCTS,
        ),
        layout=kwargs.get(
            "layout",
            HomeSectionLayout.GRID,
        ),
        config=kwargs.get(
            "config",
            {},
        ),
        order=kwargs.get(
            "order",
            1,
        ),
        is_active=kwargs.get(
            "is_active",
            True,
        ),
    )


def create_hero_slide(**kwargs):

    section = kwargs.pop(
        "section",
        None,
    )

    if section is None:
        section = create_home_section(
            section_type=HomeSectionType.HERO_SLIDER,
        )

    return HeroSlide.objects.create(
        section=section,
        title=kwargs.get(
            "title",
            "اسلاید تست",
        ),
        subtitle=kwargs.get(
            "subtitle",
            "",
        ),
        desktop_image=kwargs.get(
            "desktop_image",
            "home/hero/test.jpg",
        ),
        mobile_image=kwargs.get(
            "mobile_image",
            "",
        ),
        button_text=kwargs.get(
            "button_text",
            "",
        ),
        button_url=kwargs.get(
            "button_url",
            "",
        ),
        order=kwargs.get(
            "order",
            1,
        ),
        is_active=kwargs.get(
            "is_active",
            True,
        ),
    )


def create_banner(**kwargs):

    section = kwargs.pop(
        "section",
        None,
    )

    if section is None:
        section = create_home_section(
            section_type=HomeSectionType.BANNER,
        )

    return Banner.objects.create(
        section=section,
        title=kwargs.get(
            "title",
            "بنر تست",
        ),
        desktop_image=kwargs.get(
            "desktop_image",
            "home/banner/test.jpg",
        ),
        mobile_image=kwargs.get(
            "mobile_image",
            "",
        ),
        url=kwargs.get(
            "url",
            "",
        ),
        order=kwargs.get(
            "order",
            1,
        ),
        is_active=kwargs.get(
            "is_active",
            True,
        ),
    )


def create_home_section_product(**kwargs):

    section = kwargs.pop(
        "section",
        None,
    )

    if section is None:
        section = create_home_section(
            section_type=HomeSectionType.CUSTOM_PRODUCTS,
        )

    product = kwargs.pop(
        "product",
        None,
    )

    if product is None:
        product = create_product()

    return HomeSectionProduct.objects.create(
        section=section,
        product=product,
        order=kwargs.get(
            "order",
            1,
        ),
    )


def create_home_section_category(**kwargs):

    section = kwargs.pop(
        "section",
        None,
    )

    if section is None:
        section = create_home_section(
            section_type=HomeSectionType.CATEGORIES,
        )

    category = kwargs.pop(
        "category",
        None,
    )

    if category is None:
        category = create_category()

    return HomeSectionCategory.objects.create(
        section=section,
        category=category,
        order=kwargs.get(
            "order",
            1,
        ),
    )


def create_home_section_brand(**kwargs):

    section = kwargs.pop(
        "section",
        None,
    )

    if section is None:
        section = create_home_section(
            section_type=HomeSectionType.BRANDS,
        )

    brand = kwargs.pop(
        "brand",
        None,
    )

    if brand is None:
        brand = create_brand()

    return HomeSectionBrand.objects.create(
        section=section,
        brand=brand,
        order=kwargs.get(
            "order",
            1,
        ),
    )


def create_hero_section(**kwargs):
    return create_home_section(
        section_type=HomeSectionType.HERO_SLIDER,
        **kwargs,
    )


def create_banner_section(**kwargs):
    return create_home_section(
        section_type=HomeSectionType.BANNER,
        **kwargs,
    )


def create_product_section(**kwargs):
    return create_home_section(
        section_type=HomeSectionType.CUSTOM_PRODUCTS,
        **kwargs,
    )


def create_featured_product_section(**kwargs):
    return create_home_section(
        section_type=HomeSectionType.FEATURED_PRODUCTS,
        **kwargs,
    )


def create_latest_product_section(**kwargs):
    return create_home_section(
        section_type=HomeSectionType.LATEST_PRODUCTS,
        **kwargs,
    )


def create_discount_product_section(**kwargs):
    return create_home_section(
        section_type=HomeSectionType.DISCOUNT_PRODUCTS,
        **kwargs,
    )


def create_best_seller_product_section(**kwargs):
    return create_home_section(
        section_type=HomeSectionType.BEST_SELLER_PRODUCTS,
        **kwargs,
    )


def create_category_section(**kwargs):
    return create_home_section(
        section_type=HomeSectionType.CATEGORIES,
        **kwargs,
    )


def create_brand_section(**kwargs):
    return create_home_section(
        section_type=HomeSectionType.BRANDS,
        **kwargs,
    )