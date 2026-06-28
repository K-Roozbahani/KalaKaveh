from django_filters import rest_framework as filters

from products.models import Product


class ProductFilter(filters.FilterSet):
    """
    فیلتر محصولات فروشگاه
    """

    min_price = filters.NumberFilter(method="filter_min_price")
    max_price = filters.NumberFilter(method="filter_max_price")

    brand = filters.NumberFilter(field_name="brand_id")
    category = filters.NumberFilter(field_name="category_id")

    has_stock = filters.BooleanFilter(method="filter_has_stock")

    class Meta:
        model = Product

        fields = [
            "brand",
            "category",
        ]

    def filter_min_price(self, queryset, name, value):
        """
        حداقل قیمت (بر اساس variant پیش‌فرض)
        """

        return queryset.filter(
            variants__final_price__gte=value,
            variants__is_active=True,
        ).distinct()

    def filter_max_price(self, queryset, name, value):
        """
        حداکثر قیمت (بر اساس variant پیش‌فرض)
        """

        return queryset.filter(
            variants__final_price__lte=value,
            variants__is_active=True,
        ).distinct()

    def filter_has_stock(self, queryset, name, value):
        """
        فیلتر موجودی
        """

        if value:
            return queryset.filter(
                variants__stock__gt=0,
                variants__is_active=True,
            ).distinct()

        return queryset