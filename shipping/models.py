from django.db import models
from django.utils.translation import gettext_lazy as _

from shipping.constants import ShipmentStatus


class ShippingMethodQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class ShippingMethod(models.Model):
    name = models.CharField(
        verbose_name=_("نام روش ارسال"),
        max_length=100,
    )

    code = models.CharField(
        verbose_name=_("کد روش ارسال"),
        max_length=50,
        unique=True,
    )

    price = models.PositiveIntegerField(
        verbose_name=_("هزینه ارسال"),
    )

    estimated_days = models.PositiveSmallIntegerField(
        verbose_name=_("زمان تقریبی تحویل (روز)"),
    )

    is_active = models.BooleanField(
        verbose_name=_("فعال"),
        default=True,
    )

    created_at = models.DateTimeField(
        verbose_name=_("تاریخ ایجاد"),
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        verbose_name=_("تاریخ بروزرسانی"),
        auto_now=True,
    )

    objects = ShippingMethodQuerySet.as_manager()

    class Meta:
        verbose_name = _("روش ارسال")
        verbose_name_plural = _("روش‌های ارسال")
        ordering = ("name",)

    def __str__(self):
        return self.name


class ShipmentQuerySet(models.QuerySet):
    def pending(self):
        return self.filter(status=ShipmentStatus.PENDING)

    def packaged(self):
        return self.filter(status=ShipmentStatus.PACKAGED)

    def shipped(self):
        return self.filter(status=ShipmentStatus.SHIPPED)

    def delivered(self):
        return self.filter(status=ShipmentStatus.DELIVERED)

    def returned(self):
        return self.filter(status=ShipmentStatus.RETURNED)

    def canceled(self):
        return self.filter(status=ShipmentStatus.CANCELED)


class Shipment(models.Model):
    order = models.OneToOneField(
        "orders.Order",
        verbose_name=_("سفارش"),
        on_delete=models.PROTECT,
        related_name="shipment",
    )

    shipping_method = models.ForeignKey(
        "shipping.ShippingMethod",
        verbose_name=_("روش ارسال"),
        on_delete=models.PROTECT,
        related_name="shipments",
    )

    tracking_code = models.CharField(
        verbose_name=_("کد رهگیری"),
        max_length=100,
        blank=True,
    )

    status = models.CharField(
        verbose_name=_("وضعیت"),
        max_length=20,
        choices=ShipmentStatus.choices,
        default=ShipmentStatus.PENDING,
    )

    shipped_at = models.DateTimeField(
        verbose_name=_("زمان ارسال"),
        null=True,
        blank=True,
    )

    delivered_at = models.DateTimeField(
        verbose_name=_("زمان تحویل"),
        null=True,
        blank=True,
    )

    description = models.TextField(
        verbose_name=_("توضیحات"),
        blank=True,
    )

    created_at = models.DateTimeField(
        verbose_name=_("تاریخ ایجاد"),
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        verbose_name=_("تاریخ بروزرسانی"),
        auto_now=True,
    )

    objects = ShipmentQuerySet.as_manager()

    class Meta:
        verbose_name = _("مرسوله")
        verbose_name_plural = _("مرسوله‌ها")
        ordering = ("-created_at",)

    def __str__(self):
        return f"Shipment - {self.order.order_number}"

