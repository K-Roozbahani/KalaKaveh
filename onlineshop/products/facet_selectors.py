from django.db.models import Max, Min, Q

from products.models import Product


class ProductFacetSelector:
    """
    سلکتور مربوط به استخراج اطلاعات فیلترهای محصولات.
    """

    @classmethod
    def get_facets(cls, queryset):
        """
        استخراج تمامی Facet های مورد نیاز برای لیست محصولات.

        توجه:
            queryset باید بعد از اعمال تمامی فیلترها و جستجو و
            قبل از Pagination ارسال شود.
        """
        return {
            "categories": cls.get_categories(queryset),
            "brands": cls.get_brands(queryset),
            "price": cls.get_price(queryset),
        }

    @staticmethod
    def get_categories(queryset):
        """
        استخراج دسته‌بندی‌های موجود در QuerySet.
        """
        return list(
            queryset.values_list(
                "category__name",
                flat=True,
            )
            .distinct()
            .order_by("category__name")
        )

    @staticmethod
    def get_brands(queryset):
        """
        استخراج برندهای موجود در QuerySet.
        """
        return list(
            queryset.values_list(
                "brand__name",
                flat=True,
            )
            .distinct()
            .order_by("brand__name")
        )

    @staticmethod
    def get_price(queryset):
        """
        استخراج بازه قیمت محصولات.

        قیمت‌ها بر اساس Variant های فعال محاسبه می‌شوند.
        """

        prices = queryset.aggregate(
            min=Min("default_price"),
            max=Max("default_price"),
        )

        return {
            "min": prices["min"],
            "max": prices["max"],
        }