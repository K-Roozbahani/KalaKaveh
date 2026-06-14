from django.db import models
from django.db.models import Q
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _

from apps.orders.models import Order

from .constants import (
    GatewayType,
    PaymentStatus,
)


class Payment(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        related_name="payments",
        verbose_name=_("سفارش"),
    )

    gateway = models.CharField(
        _("درگاه پرداخت"),
        max_length=20,
        choices=GatewayType.choices,
        db_index=True,
    )

    authority = models.CharField(
        _("کد Authority"),
        max_length=255,
        unique=True,
        blank=True,
        db_index=True,
    )

    ref_id = models.CharField(
        _("شماره مرجع پرداخت"),
        max_length=255,
        blank=True,
    )

    amount = models.DecimalField(
        _("مبلغ"),
        max_digits=12,
        decimal_places=0,
    )

    status = models.CharField(
        _("وضعیت پرداخت"),
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        db_index=True,
    )

    failure_reason = models.TextField(
        _("دلیل خطا"),
        blank=True,
    )

    paid_at = models.DateTimeField(
        _("زمان پرداخت"),
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        _("تاریخ ایجاد"),
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        _("تاریخ بروزرسانی"),
        auto_now=True,
    )

    class Meta:
        verbose_name = _("پرداخت")
        verbose_name_plural = _("پرداخت‌ها")

        ordering = [
            "-created_at",
        ]

        indexes = [
            models.Index(
                fields=["status"],
                name="payment_status_idx",
            ),
            models.Index(
                fields=["created_at"],
                name="payment_created_idx",
            ),
            models.Index(
                fields=["gateway"],
                name="payment_gateway_idx",
            ),
        ]

        constraints = [
            UniqueConstraint(
                fields=["order"],
                condition=Q(
                    status=PaymentStatus.SUCCESS,
                ),
                name="unique_success_payment_per_order",
            ),
        ]

    def __str__(self):
        return (
            f"{self.order.order_code}"
            f" - "
            f"{self.get_status_display()}"
        )