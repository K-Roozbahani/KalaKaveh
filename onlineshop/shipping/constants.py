from django.db import models
from django.utils.translation import gettext_lazy as _


class ShipmentStatus(models.TextChoices):
    PENDING = "PENDING", _("در انتظار آماده‌سازی")
    PACKAGED = "PACKAGED", _("بسته‌بندی شده")
    SHIPPED = "SHIPPED", _("ارسال شده")
    DELIVERED = "DELIVERED", _("تحویل شده")
    RETURNED = "RETURNED", _("مرجوع شده")
    CANCELED = "CANCELED", _("لغو شده")