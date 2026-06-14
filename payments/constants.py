from django.db import models


class PaymentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SUCCESS = "success", "Success"
    FAILED = "failed", "Failed"
    CANCELED = "canceled", "Canceled"
    REFUNDED = "refunded", "Refunded"


class GatewayType(models.TextChoices):
    ZARINPAL = "zarinpal", "Zarinpal"