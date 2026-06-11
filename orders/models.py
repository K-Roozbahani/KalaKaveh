from django.db import models

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from orders.constants import OrderStatus
from orders.managers import OrderManager


class Order(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name=_("کاربر"),
    )

    order_number = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        verbose_name=_("شماره سفارش"),
    )

    status = models.CharField(
        max_length=20,
        choices=OrderStatus.CHOICES,
        default=OrderStatus.PENDING,
        db_index=True,
        verbose_name=_("وضعیت"),
    )

    address_snapshot = models.JSONField(
        verbose_name=_("اسنپ شات آدرس"),
    )

    subtotal = models.DecimalField(
        max_digits=14,
        decimal_places=0,
        verbose_name=_("جمع کالاها"),
    )

    discount_amount = models.DecimalField(
        max_digits=14,
        decimal_places=0,
        default=0,
        verbose_name=_("مبلغ تخفیف"),
    )

    shipping_cost = models.DecimalField(
        max_digits=14,
        decimal_places=0,
        default=0,
        verbose_name=_("هزینه ارسال"),
    )

    total_amount = models.DecimalField(
        max_digits=14,
        decimal_places=0,
        verbose_name=_("مبلغ نهایی"),
    )

    note = models.TextField(
        blank=True,
        verbose_name=_("یادداشت مشتری"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    objects = OrderManager()

    class Meta:
        verbose_name = _("سفارش")
        verbose_name_plural = _("سفارش‌ها")
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.order_number

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("سفارش"),
    )

    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        related_name="+",
        verbose_name=_("محصول"),
    )

    variant = models.ForeignKey(
        "products.ProductVariant",
        on_delete=models.PROTECT,
        related_name="+",
        verbose_name=_("تنوع محصول"),
    )

    quantity = models.PositiveIntegerField(
        verbose_name=_("تعداد"),
    )

    price = models.DecimalField(
        max_digits=14,
        decimal_places=0,
        verbose_name=_("قیمت واحد"),
    )

    discount_amount = models.DecimalField(
        max_digits=14,
        decimal_places=0,
        default=0,
        verbose_name=_("تخفیف واحد"),
    )

    final_price = models.DecimalField(
        max_digits=14,
        decimal_places=0,
        verbose_name=_("قیمت نهایی واحد"),
    )

    product_snapshot = models.JSONField(
        verbose_name=_("اسنپ شات محصول"),
    )

    class Meta:
        verbose_name = _("آیتم سفارش")
        verbose_name_plural = _("آیتم‌های سفارش")
        constraints = [
            models.UniqueConstraint(
                fields=["order", "variant"],
                name="unique_variant_per_order",
            )
        ]

    def __str__(self):
        return f"{self.order.order_number} - {self.variant}"


