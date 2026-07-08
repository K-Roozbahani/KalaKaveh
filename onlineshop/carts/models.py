from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from carts.constants import CartStatus


class Cart(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="carts",
        null=True,
        blank=True,
        verbose_name=_("کاربر"),
    )

    session_key = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("شناسه نشست"),
        help_text=_("برای سبد خرید کاربران مهمان"),
    )

    coupon = models.ForeignKey(
        "discounts.Coupon",
        on_delete=models.SET_NULL,
        related_name="carts",
        null=True,
        blank=True,
        verbose_name=_("کد تخفیف"),
    )

    status = models.CharField(
        max_length=20,
        choices=CartStatus.CHOICES,
        default=CartStatus.ACTIVE,
        db_index=True,
        verbose_name=_("وضعیت"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("تاریخ ایجاد"),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("تاریخ آخرین بروزرسانی"),
    )

    class Meta:
        verbose_name = _("سبد خرید")
        verbose_name_plural = _("سبدهای خرید")

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=["user", "status"],
                name="cart_user_status_idx",
            ),
            models.Index(
                fields=["session_key", "status"],
                name="cart_session_status_idx",
            ),
            models.Index(
                fields=[
                    "status",
                    "updated_at",
                ],
                name="cart_status_updated_idx",
            ),
        ]

    def __str__(self):
        if self.user:
            return f"سبد خرید کاربر {self.user}"

        return f"سبد خرید مهمان #{self.pk}"


class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("سبد خرید"),
    )

    variant = models.ForeignKey(
        "products.ProductVariant",
        on_delete=models.CASCADE,
        related_name="cart_items",
        verbose_name=_("تنوع محصول"),
    )

    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_("تعداد"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("تاریخ ایجاد"),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("تاریخ آخرین بروزرسانی"),
    )

    class Meta:
        verbose_name = _("آیتم سبد خرید")
        verbose_name_plural = _("آیتم‌های سبد خرید")

        ordering = ("id",)

        constraints = [
            models.UniqueConstraint(
                fields=["cart", "variant"],
                name="unique_variant_per_cart",
            )
        ]

        indexes = [
            models.Index(
                fields=["cart"],
                name="cartitem_cart_idx",
            ),
            models.Index(
                fields=["variant"],
                name="cartitem_variant_idx",
            ),
        ]

    def __str__(self):
        return (
            f"{self.variant} "
            f"{self.quantity}(عدد)"
        )