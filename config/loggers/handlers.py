import logging

from rest_framework.views import exception_handler


logger = logging.getLogger("error")


def custom_exception_handler(exc, context):
    """
    مدیریت مرکزی Exception های DRF

    وظایف:
        - ثبت تمام Exception ها در error.log
        - حفظ رفتار پیش فرض DRF
    """

    request = context.get("request")
    view = context.get("view")

    logger.exception(
        "Unhandled exception",
        extra={
            "request": request,
            "view": view.__class__.__name__ if view else None,
        },
    )

    return exception_handler(exc, context)