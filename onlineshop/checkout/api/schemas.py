"""
Schemaهای OpenAPI مربوط به فرآیند Checkout.
"""

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from rest_framework import serializers

from checkout.api.serializers import (
    CheckoutConfirmSerializer,
    CheckoutSerializer,
    CheckoutSummarySerializer,
)


CheckoutConfirmResponseSerializer = inline_serializer(
    name="CheckoutConfirmResponse",
    fields={
        "payment_url": serializers.URLField(
            help_text="آدرس درگاه پرداخت.",
        ),
    },
)


schema_checkout = extend_schema_view(
    list=extend_schema(
        summary="نمایش اطلاعات Checkout",
        description=(
            "دریافت خلاصه اطلاعات Checkout "
            "برای کاربر احراز هویت‌شده."
        ),
        responses={
            200: CheckoutSummarySerializer,
        },
        tags=["Checkout"],
    ),
    create=extend_schema(
        summary="بروزرسانی Checkout",
        description=(
            "دریافت اطلاعات Checkout بر اساس "
            "اطلاعات ارسال‌شده و بروزرسانی فرآیند خرید."
        ),
        request=CheckoutSerializer,
        responses={
            200: CheckoutSummarySerializer,
        },
        tags=["Checkout"],
    ),
    confirm=extend_schema(
        summary="تأیید نهایی Checkout",
        description=(
            "تأیید نهایی Checkout و ایجاد فرآیند پرداخت "
            "برای سفارش."
        ),
        request=CheckoutConfirmSerializer,
        responses={
            201: CheckoutConfirmResponseSerializer,
        },
        tags=["Checkout"],
    ),
)