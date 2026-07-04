from django.db import models
from django.utils.translation import gettext_lazy as _

from shipping.constants import ShipmentStatus, ShippingRuleAttribute
from shipping.managers import ShippingMethodQuerySet, ShipmentQuerySet

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

    # price = models.PositiveIntegerField(
    #     verbose_name=_("هزینه ارسال"),
    # )
    #
    # estimated_days = models.PositiveSmallIntegerField(
    #     verbose_name=_("زمان تقریبی تحویل (روز)"),
    # )

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


class ShippingRule(models.Model):
    """
    قانون ارسال

    هر Rule مشخص می‌کند که برای یک روش ارسال،
    در چه منطقه‌ای و با چه شرایطی، چه هزینه‌ای دریافت شود.
    """

    shipping_method = models.ForeignKey(
        ShippingMethod,
        verbose_name=_("روش ارسال"),
        on_delete=models.CASCADE,
        related_name="rules",
    )

    province = models.ForeignKey(
        "addresses.Province",
        verbose_name=_("استان"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="shipping_rules",
    )

    city = models.ForeignKey(
        "addresses.City",
        verbose_name=_("شهر"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="shipping_rules",
    )

    rule_type = models.CharField(
        verbose_name=_("نوع قانون"),
        max_length=20,
        choices=ShippingRuleAttribute.choices,
        default=ShippingRuleAttribute.DEFAULT,
    )

    price = models.PositiveIntegerField(
        _("هزینه ارسال"),
    )

    estimated_days = models.PositiveSmallIntegerField(
        _("مدت تقریبی ارسال (روز)"),
        default=1,
    )

    priority = models.PositiveSmallIntegerField(
        _("اولویت"),
        default=100,
        help_text=_("اعداد کمتر اولویت بالاتری دارند."),
    )

    is_active = models.BooleanField(
        _("فعال"),
        default=True,
    )

    class Meta:
        verbose_name = _("قانون ارسال")
        verbose_name_plural = _("قوانین ارسال")
        ordering = (
            "priority",
            "id",
        )

    def __str__(self):
        location = self.city or self.province or _("سراسری")

        return f"{self.shipping_method} - {location}"

