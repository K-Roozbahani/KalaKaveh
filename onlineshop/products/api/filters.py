from django_filters import rest_framework as filters

from products.models import Product
from products.selectors import (
    get_category_by_slug,
    get_category_descendants,
)



class ProductFilter(filters.FilterSet):
    """
    فیلتر محصولات فروشگاه
    """

    min_price = filters.NumberFilter(method="filter_min_price")
    max_price = filters.NumberFilter(method="filter_max_price")

    brand = filters.CharFilter(field_name="brand__slug")
    category = filters.CharFilter(method="filter_category")

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

def filter_category(self, queryset, name, value):
    """
    فیلتر محصولات بر اساس دسته‌بندی و تمام زیرمجموعه‌های آن.
    """

    category = get_category_by_slug(slug=value)

    if category is None:
        return queryset.none()

    categories = get_category_descendants(category=category)

    return queryset.filter(
        category__in=categories,
    )