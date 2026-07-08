"""
Formatter های سفارشی پروژه

این ماژول مسئول آماده‌سازی LogRecord قبل از ثبت در فایل‌های Log است.
در صورتی که برخی از فیلدهای سفارشی وجود نداشته باشند،
مقدار پیش‌فرض برای آن‌ها قرار می‌دهد تا فرآیند Logging
هیچ‌گاه با خطا مواجه نشود.
"""

from logging import Formatter


class ProductionFormatter(Formatter):
    """
    Formatter استاندارد پروژه برای محیط Production.
    """

    DEFAULT_FIELDS = {
        "request_id": "-",
        "request_path": "-",
        "request_method": "-",
        "user_id": "-",
        "ip": "-",
        "view": "-",
        "order_id": "-",
        "payment_id": "-",
        "shipment_id": "-",
        "cart_id": "-",
        "coupon_code": "-",
        "gateway": "-",
    }

    def format(self, record):
        """
        قبل از Format شدن LogRecord، تمام فیلدهای سفارشی
        در صورت نبود مقداردهی اولیه می‌شوند.
        """

        for field, default in self.DEFAULT_FIELDS.items():
            if not hasattr(record, field):
                setattr(record, field, default)

        return super().format(record)