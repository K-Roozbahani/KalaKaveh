from django.contrib import admin

from home.models import (
    Banner,
    HeroSlide,
    HomeSection,
    HomeSectionBrand,
    HomeSectionCategory,
    HomeSectionProduct,
)


class HeroSlideInline(admin.TabularInline):
    model = HeroSlide
    extra = 0
    show_change_link = True


class BannerInline(admin.TabularInline):
    model = Banner
    extra = 0
    show_change_link = True


class ProductInline(admin.TabularInline):
    model = HomeSectionProduct
    extra = 0
    autocomplete_fields = ("product",)
    show_change_link = True


class CategoryInline(admin.TabularInline):
    model = HomeSectionCategory
    extra = 0
    autocomplete_fields = ("category",)
    show_change_link = True


class BrandInline(admin.TabularInline):
    model = HomeSectionBrand
    extra = 0
    autocomplete_fields = ("brand",)
    show_change_link = True
# ___________________________________________________
#               ADMIN
# __________________________________________________

@admin.register(HomeSection)
class HomeSectionAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "section_type",
        "layout",
        "order",
        "is_active",
    )

    list_filter = (
        "section_type",
        "layout",
        "is_active",
    )

    search_fields = (
        "title",
    )

    list_editable = (
        "order",
        "is_active",
    )

    ordering = (
        "order",
    )


    def get_inline_instances(
        self,
        request,
        obj=None,
    ):
        if obj is None:
            return []

        inline_classes = []

        match obj.section_type:

            case "hero_slider":
                inline_classes = [
                    HeroSlideInline,
                ]

            case "banner":
                inline_classes = [
                    BannerInline,
                ]

            case "brands":
                inline_classes = [
                    BrandInline,
                ]

            case "categories":
                inline_classes = [
                    CategoryInline,
                ]

            case _:
                inline_classes = [
                    ProductInline,
                ]

        return [
            inline(self.model, self.admin_site)
            for inline in inline_classes
        ]
