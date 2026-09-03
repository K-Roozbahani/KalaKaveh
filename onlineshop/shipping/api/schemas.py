"""
Schemaهای OpenAPI مربوط به ارسال و مرسوله‌ها.
"""

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

from shipping.api.serializers import (
    ShipmentDetailSerializer,
    ShipmentListSerializer,
    ShippingMethodSerializer,
)


schema_shipping_method = extend_schema_view(
    list=extend_schema(
        summary="لیست روش‌های ارسال",
        description=(
            "دریافت لیست روش‌های ارسال فعال "
            "قابل انتخاب برای کاربر."
        ),
        responses={
            200: ShippingMethodSerializer(many=True),
        },
        tags=["ارسال"],
    ),
    retrieve=extend_schema(
        summary="جزئیات روش ارسال",
        description=(
            "دریافت جزئیات یک روش ارسال فعال."
        ),
        responses={
            200: ShippingMethodSerializer,
        },
        tags=["ارسال"],
    ),
)


schema_shipment = extend_schema_view(
    list=extend_schema(
        summary="لیست مرسوله‌های کاربر",
        description=(
            "دریافت لیست مرسوله‌های متعلق "
            "به کاربر احراز هویت‌شده."
        ),
        responses={
            200: ShipmentListSerializer(many=True),
        },
        tags=["مرسوله‌ها"],
    ),
    retrieve=extend_schema(
        summary="جزئیات مرسوله",
        description=(
            "دریافت جزئیات یک مرسوله متعلق "
            "به کاربر احراز هویت‌شده."
        ),
        responses={
            200: ShipmentDetailSerializer,
        },
        tags=["مرسوله‌ها"],
    ),
)