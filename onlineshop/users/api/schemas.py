"""
Schemaهای OpenAPI مربوط به API کاربران.

در این فایل مستندات endpointهای کاربران از منطق
ViewSet جدا شده‌اند تا Viewها خواناتر و قابل نگهداری‌تر باشند.
"""

from drf_spectacular.utils import extend_schema, extend_schema_view


USER_TAG = "کاربران"
ACCOUNT_TAG = "حساب کاربری"


user_api_schema = extend_schema_view(
    list=extend_schema(
        tags=[USER_TAG],
        summary="دریافت لیست کاربران",
        description="دریافت لیست کاربران سیستم.",
    ),
    create=extend_schema(
        tags=[USER_TAG],
        summary="ایجاد کاربر",
        description="ایجاد یک کاربر جدید در سیستم.",
    ),
    retrieve=extend_schema(
        tags=[USER_TAG],
        summary="دریافت اطلاعات کاربر",
        description="دریافت اطلاعات یک کاربر بر اساس شماره تلفن.",
    ),
    update=extend_schema(
        tags=[USER_TAG],
        summary="ویرایش کامل کاربر",
        description="ویرایش کامل اطلاعات یک کاربر.",
    ),
    partial_update=extend_schema(
        tags=[USER_TAG],
        summary="ویرایش بخشی از اطلاعات کاربر",
        description="ویرایش بخشی از اطلاعات یک کاربر.",
    ),
    destroy=extend_schema(
        tags=[USER_TAG],
        summary="حذف کاربر",
        description="حذف یک کاربر از سیستم.",
    ),
    me=extend_schema(
        tags=[ACCOUNT_TAG],
        summary="دریافت اطلاعات حساب کاربری",
        description="دریافت اطلاعات کاربر احراز هویت‌شده فعلی.",
    ),
)