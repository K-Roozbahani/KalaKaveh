"""
Filter های سفارشی پروژه

این Filterها مسئول افزودن اطلاعات مشترک به تمام LogRecordها هستند.
"""

from logging import Filter


class RequestContextFilter(Filter):
    """
    اطلاعات مربوط به Request را به LogRecord اضافه می‌کند.

    در حال حاضر مقادیر پیش‌فرض قرار می‌گیرند و پس از
    پیاده‌سازی Middleware، اطلاعات واقعی جایگزین خواهند شد.
    """

    def filter(self, record):
        """
        افزودن اطلاعات Context به LogRecord
        """

        if not hasattr(record, "request_id"):
            record.request_id = "-"

        if not hasattr(record, "request_path"):
            record.request_path = "-"

        if not hasattr(record, "request_method"):
            record.request_method = "-"

        if not hasattr(record, "user_id"):
            record.user_id = "-"

        if not hasattr(record, "ip"):
            record.ip = "-"

        if not hasattr(record, "view"):
            record.view = "-"

        return True