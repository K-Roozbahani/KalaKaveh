"""
Exception Handler مرکزی پروژه

این ماژول مسئول ثبت Exceptionهای DRF و Django در سیستم Logging
و حفظ رفتار استاندارد DRF است.
"""

import logging

from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.views import exception_handler


logger = logging.getLogger("error")


def custom_exception_handler(exc, context):
    """
    مدیریت مرکزی Exceptionهای API.

    ValidationErrorهای Django که در Service Layer و
    Domain Layer ایجاد می‌شوند، به ValidationError استاندارد
    DRF تبدیل می‌شوند تا به‌صورت HTTP 400 به کلاینت برگردند.
    """

    request = context.get("request")
    view = context.get("view")

    logger.exception(
        str(exc),
        extra={
            "request_path": request.path if request else "-",
            "request_method": request.method if request else "-",
            "user_id": (
                request.user.pk
                if request
                and hasattr(request, "user")
                and request.user.is_authenticated
                else "-"
            ),
            "view": view.__class__.__name__ if view else "-",
        },
    )

    if isinstance(exc, DjangoValidationError):
        exc = DRFValidationError(
            detail=exc.messages,
        )

    return exception_handler(
        exc,
        context,
    )