from django.utils.translation import gettext_lazy as _


class OrderStatus:
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELED = "canceled"

    CHOICES = (
        (PENDING, _("در انتظار پرداخت")),
        (CONFIRMED, _("تایید شده")),
        (PROCESSING, _("در حال آماده سازی")),
        (COMPLETED, _("تکمیل شده")),
        (CANCELED, _("لغو شده")),
    )