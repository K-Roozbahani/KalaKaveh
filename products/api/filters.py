import django_filters
from ..models import Product, ProductVariant


class ProductFilter(django_filters.FilterSet):
    """
    فیلتر محصولات
    """

    name = django_filters.CharFilter(lookup_expr="icontains")
    category = django_filters.NumberFilter()
    brand = django_filters.NumberFilter()
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = Product
        fields = ["name", "category", "brand", "is_active"]


class VariantFilter(django_filters.FilterSet):
    """
    فیلتر واریانت‌ها
    """

    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    in_stock = django_filters.BooleanFilter(method="filter_in_stock")

    class Meta:
        model = ProductVariant
        fields = ["price_min", "price_max"]

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset