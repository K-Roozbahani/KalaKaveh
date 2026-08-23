"""
Schemaهای OpenAPI مربوط به پرداخت‌ها.
"""

from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from rest_framework import serializers

from payments.api.serializers import (
    PaymentDetailSerializer,
    PaymentListSerializer,
)


PaymentCreateResponseSerializer = inline_serializer(
    name="PaymentCreateResponse",
    fields={
        "payment_url": serializers.URLField(
            help_text="آدرس درگاه پرداخت.",
        ),
        "authority": serializers.CharField(
            help_text="شناسه یکتای پرداخت در درگاه.",
        ),
    },
)


schema_payment = extend_schema_view(
    list=extend_schema(
        summary="لیست پرداخت‌های کاربر",
        description="دریافت لیست پرداخت‌های کاربر احراز هویت‌شده.",
        responses={
            200: PaymentListSerializer(many=True),
        },
        tags=["پرداخت‌ها"],
    ),
    retrieve=extend_schema(
        summary="جزئیات پرداخت",
        description="دریافت جزئیات یک پرداخت متعلق به کاربر.",
        responses={
            200: PaymentDetailSerializer,
        },
        tags=["پرداخت‌ها"],
    ),
    create=extend_schema(
        summary="ایجاد پرداخت",
        description=(
            "ایجاد یک پرداخت برای سفارش کاربر و دریافت "
            "آدرس درگاه پرداخت."
        ),
        responses={
            201: PaymentCreateResponseSerializer,
        },
        tags=["پرداخت‌ها"],
    ),
)


schema_payment_callback = extend_schema(
    summary="Callback درگاه پرداخت",
    description=(
        "دریافت نتیجه بازگشت کاربر از درگاه پرداخت "
        "و پردازش وضعیت پرداخت."
    ),
    parameters=[
        OpenApiParameter(
            name="Authority",
            type=str,
            location=OpenApiParameter.QUERY,
            required=True,
            description="شناسه پرداخت ارسال‌شده توسط درگاه.",
        ),
    ],
    responses={
        200: PaymentDetailSerializer,
        400: OpenApiResponse(
            description="پارامتر Authority ارسال نشده یا نامعتبر است.",
        ),
    },
    tags=["پرداخت‌ها"],
)