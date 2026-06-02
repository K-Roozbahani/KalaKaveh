# cart/models.py
import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from products.models import Product, ProductAttributeValue


class Cart(models.Model):
    id = models.UUIDField(_("شناسه سبد"), primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("کاربر"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='cart'
    )
    session_id = models.CharField(_("شناسه نشست"), max_length=255, null=True, blank=True, db_index=True)
    is_active = models.BooleanField(_("فعال"), default=True)
    created_at = models.DateTimeField(_("تاریخ ایجاد"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاریخ بروزرسانی"), auto_now=True)

    class Meta:
        verbose_name = _("سبد خرید")
        verbose_name_plural = _("سبدهای خرید")
        indexes = [
            models.Index(fields=['session_id']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"سبد خرید - {self.user or self.session_id}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        verbose_name=_("سبد خرید"),
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        verbose_name=_("محصول"),
        on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField(
        _("تعداد"),
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(1000)]
    )
    unit_price = models.DecimalField(_("قیمت واحد"), max_digits=10, decimal_places=2)
    product_name_snapshot = models.CharField(_("نام محصول"), max_length=255)
    total_price = models.DecimalField(_("قیمت کل"), max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(_("تاریخ ایجاد"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاریخ بروزرسانی"), auto_now=True)

    class Meta:
        verbose_name = _("آیتم سبد خرید")
        verbose_name_plural = _("آیتم‌های سبد خرید")
        unique_together = ('cart', 'product')

    def save(self, *args, **kwargs):
        if self.product:
            self.product_name_snapshot = self.product.name
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_name_snapshot} x {self.quantity}"


class CartItemAttribute(models.Model):
    cart_item = models.ForeignKey(
        CartItem,
        verbose_name=_("آیتم سبد"),
        related_name='item_attributes',
        on_delete=models.CASCADE
    )
    attribute_value = models.ForeignKey(
        ProductAttributeValue,
        verbose_name=_("مقدار ویژگی"),
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = _("ویژگی آیتم سبد")
        verbose_name_plural = _("ویژگی‌های آیتم سبد")
        unique_together = ('cart_item', 'attribute_value')

    def __str__(self):
        return f"{self.cart_item} - {self.attribute_value}"
