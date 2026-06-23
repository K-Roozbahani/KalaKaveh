import django_filters
from ..models import Product, ProductVariant


class ProductFilter(django_filters.FilterSet):
    """
    فیلتر محصولات
    """

    name = django_filters.CharFilter(lookup_expr="icontains")
    category = django_filters.CharFilter(
        field_name="category__slug",
    )

    brand = django_filters.CharFilter(
        field_name="brand__slug",
    )

    slug = django_filters.CharFilter(
        lookup_expr="icontains",
    )

    created_after = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
    )

    created_before = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
    )

    is_active = django_filters.BooleanFilter()

    class Meta:
        model = Product
        fields = ["name", "category", "brand", "is_active", "slug", "created_after", "created_before"]


class VariantFilter(django_filters.FilterSet):
    """
    فیلتر واریانت‌ها
    """

    price_min = django_filters.NumberFilter(
        field_name="final_price",
        lookup_expr="gte",
    )

    price_max = django_filters.NumberFilter(
        field_name="final_price",
        lookup_expr="lte",
    )

    is_active = django_filters.BooleanFilter()
    in_stock = django_filters.BooleanFilter(method="filter_in_stock")

    class Meta:
        model = ProductVariant
        fields = ["price_min", "price_max", "is_active", "in_stock"]

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset