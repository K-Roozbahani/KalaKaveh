"""
Schemaهای OpenAPI مربوط به سفارش‌ها.
"""

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

from orders.api.serializers import (
    OrderDetailSerializer,
    OrderItemSerializer,
    OrderListSerializer,
)


schema_order = extend_schema_view(
    list=extend_schema(
        summary="لیست سفارش‌های کاربر",
        description=(
            "دریافت لیست سفارش‌های متعلق به کاربر "
            "احراز هویت‌شده."
        ),
        responses={
            200: OrderListSerializer(many=True),
        },
        tags=["سفارش‌ها"],
    ),
    retrieve=extend_schema(
        summary="جزئیات سفارش",
        description=(
            "دریافت جزئیات یک سفارش بر اساس "
            "شماره سفارش."
        ),
        responses={
            200: OrderDetailSerializer,
        },
        tags=["سفارش‌ها"],
    ),
    items=extend_schema(
        summary="اقلام سفارش",
        description=(
            "دریافت لیست اقلام یک سفارش "
            "بر اساس شماره سفارش."
        ),
        responses={
            200: OrderItemSerializer(many=True),
        },
        tags=["سفارش‌ها"],
    ),
)