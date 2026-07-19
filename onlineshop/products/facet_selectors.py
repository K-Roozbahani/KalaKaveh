from django.db.models import Count, Max, Min, F


class ProductFacetSelector:
    """
    سلکتور مربوط به استخراج اطلاعات فیلترهای محصولات.
    """

    @classmethod
    def get_facets(cls, queryset):
        """
        استخراج Facet های مورد نیاز برای صفحه لیست محصولات.

        نکته:
            queryset باید پس از اعمال تمامی فیلترها و جستجو
            و قبل از Pagination ارسال شود.
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
            queryset.values(
                "category__name",
                "category__slug",
            )
            .annotate(
                count=Count("id"),
            )
            .order_by("count")
        )

    @staticmethod
    def get_brands(queryset):
        """
        استخراج برندهای موجود در QuerySet.
        """

        return list(
            queryset.values(
                "brand__name",
                "brand__slug",
            )
            .annotate(
                count=Count("id"),
            )
            .order_by("count")
        )

    @staticmethod
    def get_price(queryset):
        """
        استخراج بازه قیمت محصولات.
        """

        prices = queryset.aggregate(
            min=Min("default_price"),
            max=Max("default_price"),
        )

        return {
            "min": prices["min"],
            "max": prices["max"],
        }