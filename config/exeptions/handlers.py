"""
Exception Handler مرکزی پروژه

این ماژول مسئول ثبت Exceptionهای DRF در سیستم Logging
و حفظ رفتار پیش‌فرض DRF است.
"""

import logging

from rest_framework.views import exception_handler


logger = logging.getLogger("error")


def custom_exception_handler(exc, context):
    """
    مدیریت مرکزی Exceptionهای DRF.
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

    return exception_handler(exc, context)