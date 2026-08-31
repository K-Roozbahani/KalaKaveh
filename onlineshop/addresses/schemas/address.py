"""
Schemaهای OpenAPI مربوط به آدرس‌ها.
"""

from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from rest_framework import serializers

from addresses.api.serializers import (
    AddressCreateSerializer,
    AddressDetailSerializer,
    AddressListSerializer,
    AddressUpdateSerializer,
)


schema_address = extend_schema_view(
    list=extend_schema(
        summary="لیست آدرس‌های کاربر",
        description="دریافت لیست تمام آدرس‌های کاربر احراز هویت‌شده.",
        responses={
            200: AddressListSerializer(many=True),
        },
        tags=["آدرس‌ها"],
    ),
    retrieve=extend_schema(
        summary="جزئیات آدرس",
        description="دریافت جزئیات یک آدرس متعلق به کاربر.",
        responses={
            200: AddressDetailSerializer,
        },
        tags=["آدرس‌ها"],
    ),
    create=extend_schema(
        summary="ایجاد آدرس",
        description="ایجاد یک آدرس جدید برای کاربر احراز هویت‌شده.",
        request=AddressCreateSerializer,
        responses={
            201: AddressDetailSerializer,
        },
        tags=["آدرس‌ها"],
    ),
    update=extend_schema(
        summary="ویرایش کامل آدرس",
        description="ویرایش کامل اطلاعات یک آدرس.",
        request=AddressUpdateSerializer,
        responses={
            200: AddressDetailSerializer,
        },
        tags=["آدرس‌ها"],
    ),
    partial_update=extend_schema(
        summary="ویرایش آدرس",
        description="ویرایش بخشی از اطلاعات یک آدرس.",
        request=AddressUpdateSerializer,
        responses={
            200: AddressDetailSerializer,
        },
        tags=["آدرس‌ها"],
    ),
    destroy=extend_schema(
        summary="حذف آدرس",
        description="حذف یک آدرس متعلق به کاربر.",
        responses={
            204: OpenApiResponse(
                description="آدرس با موفقیت حذف شد.",
            ),
        },
        tags=["آدرس‌ها"],
    ),
    set_default=extend_schema(
        summary="تعیین آدرس پیش‌فرض",
        description="یک آدرس را به عنوان آدرس پیش‌فرض کاربر تعیین می‌کند.",
        request=None,
        responses={
            200: inline_serializer(
                name="SetDefaultAddressResponse",
                fields={
                    "message": serializers.CharField(
                        help_text="پیام نتیجه عملیات.",
                    ),
                    "address_id": serializers.IntegerField(
                        help_text="شناسه آدرس تعیین‌شده به عنوان پیش‌فرض.",
                    ),
                },
            ),
        },
        tags=["آدرس‌ها"],
    ),
)