"""
Schemaهای OpenAPI مربوط به API احراز هویت.

در این فایل مستندات endpointهای احراز هویت از منطق
ViewSet جدا شده‌اند تا Viewها خواناتر و قابل نگهداری‌تر باشند.
"""

from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)

from authentication.api.serializers import (
    RequestOTPSerializer,
    VerifyOTPSerializer,
)


AUTHENTICATION_TAG = "احراز هویت"


authentication_api_schema = extend_schema_view(
    request_otp=extend_schema(
        summary="درخواست کد OTP",
        description=(
            "ارسال کد OTP برای شماره تلفن کاربر. "
            "این Endpoint نیاز به احراز هویت ندارد، "
            "اما به دلیل استفاده از Cookie Authentication "
            "تحت محافظت CSRF قرار دارد."
        ),
        request=RequestOTPSerializer,
        responses={
            200: OpenApiResponse(
                description="کد تأیید با موفقیت ارسال شد.",
            ),
            400: OpenApiResponse(
                description="اطلاعات ارسال‌شده معتبر نیست.",
            ),
            403: OpenApiResponse(
                description="CSRF Token نامعتبر یا ارسال نشده است.",
            ),
        },
        tags=[AUTHENTICATION_TAG],
    ),
    verify_otp=extend_schema(
        summary="تأیید OTP و ورود",
        description=(
            "کد OTP را تأیید کرده و پس از ورود موفق، "
            "Access Token و Refresh Token را به صورت "
            "HttpOnly Cookie در Response قرار می‌دهد."
        ),
        request=VerifyOTPSerializer,
        responses={
            200: OpenApiResponse(
                description=(
                    "ورود با موفقیت انجام شد و "
                    "Cookieهای احراز هویت تنظیم شدند."
                ),
            ),
            400: OpenApiResponse(
                description="کد OTP نامعتبر یا منقضی شده است.",
            ),
            403: OpenApiResponse(
                description="CSRF Token نامعتبر یا ارسال نشده است.",
            ),
        },
        tags=[AUTHENTICATION_TAG],
    ),
    refresh=extend_schema(
        summary="به‌روزرسانی Access Token",
        description=(
            "Refresh Token از HttpOnly Cookie دریافت شده و "
            "Access Token جدید صادر می‌شود. "
            "در صورت فعال بودن Rotation، Refresh Token جدید "
            "نیز صادر خواهد شد."
        ),
        request=None,
        responses={
            200: OpenApiResponse(
                description="Tokenها با موفقیت به‌روزرسانی شدند.",
            ),
            401: OpenApiResponse(
                description=(
                    "Refresh Token وجود ندارد، "
                    "منقضی شده یا نامعتبر است."
                ),
            ),
            403: OpenApiResponse(
                description="CSRF Token نامعتبر یا ارسال نشده است.",
            ),
        },
        tags=[AUTHENTICATION_TAG],
    ),
    logout=extend_schema(
        summary="خروج از حساب کاربری",
        description=(
            "Refresh Token موجود در HttpOnly Cookie را "
            "Blacklist کرده و Cookieهای احراز هویت را حذف می‌کند."
        ),
        request=None,
        responses={
            200: OpenApiResponse(
                description="کاربر با موفقیت خارج شد.",
            ),
            403: OpenApiResponse(
                description="CSRF Token نامعتبر یا ارسال نشده است.",
            ),
        },
        tags=[AUTHENTICATION_TAG],
    ),
)