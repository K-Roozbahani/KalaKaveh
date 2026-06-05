# cart/models.py
import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from products.models import Product, ProductAttributeValue, ProductVariant


class Cart(models.Model):
    """
    سبد خرید کاربر
    """

    class Status(models.TextChoices):
        ACTIVE = "active", _("فعال")
        ORDERED = "ordered", _("تبدیل شده به سفارش")
        ABANDONED = "abandoned", _("رها شده")

    id = models.UUIDField(
        _("شناسه"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("کاربر"),
        related_name="cart",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    session_id = models.CharField(
        _("شناسه نشست"),
        max_length=255,
        blank=True,
        null=True,
        db_index=True
    )

    status = models.CharField(
        _("وضعیت"),
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    coupon_code = models.CharField(
        _("کد تخفیف"),
        max_length=100,
        blank=True
    )

    shipping_price = models.PositiveBigIntegerField(
        _("هزینه ارسال"),
        default=0
    )

    discount_amount = models.PositiveBigIntegerField(
        _("مبلغ تخفیف"),
        default=0
    )

    notes = models.TextField(
        _("یادداشت مشتری"),
        blank=True
    )

    expires_at = models.DateTimeField(
        _("تاریخ انقضا"),
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        _("تاریخ ایجاد"),
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        _("تاریخ بروزرسانی"),
        auto_now=True
    )

    class Meta:
        verbose_name = _("سبد خرید")
        verbose_name_plural = _("سبدهای خرید")

        ordering = ("-created_at",)

        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["session_id"]),
            models.Index(fields=["created_at"]),
        ]

    @property
    def items_count(self):
        return self.items.count()

    @property
    def total_quantity(self):
        return sum(
            item.quantity
            for item in self.items.all()
        )

    @property
    def subtotal(self):
        return sum(
            item.total_price
            for item in self.items.all()
        )

    @property
    def total_price(self):
        return (
            self.subtotal
            - self.discount_amount
            + self.shipping_price
        )

    def __str__(self):
        return (
            self.user.get_username()
            if self.user
            else str(self.id)
        )

class CartItem(models.Model):
    """
    آیتم سبد خرید

    هر رکورد نمایانگر یک تنوع مشخص از یک محصول
    در سبد خرید کاربر است.
    """

    cart = models.ForeignKey("Cart", verbose_name=_("سبد خرید"), related_name="items", on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, verbose_name=_("تنوع محصول"), related_name="cart_items", on_delete=models.PROTECT)

    quantity = models.PositiveIntegerField(
        _("تعداد"),
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(1000)
        ]
    )

    unit_price = models.PositiveBigIntegerField(
        _("قیمت واحد")
    )

    total_price = models.PositiveBigIntegerField(
        _("قیمت کل")
    )

    product_name_snapshot = models.CharField(
        _("نام محصول"),
        max_length=255
    )

    sku_snapshot = models.CharField(
        _("کد کالا"),
        max_length=100
    )

    variant_title_snapshot = models.CharField(
        _("عنوان تنوع محصول"),
        max_length=255,
        blank=True
    )

    is_available = models.BooleanField(
        _("موجود در زمان افزودن"),
        default=True
    )

    created_at = models.DateTimeField(
        _("تاریخ ایجاد"),
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        _("تاریخ بروزرسانی"),
        auto_now=True
    )

    class Meta:
        verbose_name = _("آیتم سبد خرید")
        verbose_name_plural = _("آیتم‌های سبد خرید")

        ordering = ("-created_at",)

        constraints = [
            models.UniqueConstraint(
                fields=["cart", "variant"],
                name="unique_cart_variant"
            )
        ]

        indexes = [
            models.Index(fields=["cart"]),
            models.Index(fields=["variant"]),
            models.Index(fields=["created_at"]),
        ]

    def save(self, *args, **kwargs):

        if self.variant:

            self.product_name_snapshot = (
                self.variant.product.name
            )

            self.sku_snapshot = (
                self.variant.sku
            )

            self.unit_price = (
                self.variant.discount_price
                if self.variant.discount_price
                else self.variant.price
            )

            self.is_available = (
                self.variant.is_active
            )

            variant_values = []

            for item in self.variant.variant_attributes.select_related(
                "attribute_value",
                "attribute_value__attribute"
            ):

                variant_values.append(
                    f"{item.attribute_value.attribute.name}: "
                    f"{item.attribute_value.value}"
                )

            self.variant_title_snapshot = " | ".join(
                variant_values
            )

        self.total_price = (
            self.unit_price * self.quantity
        )

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.product_name_snapshot} "
            f"({self.variant_title_snapshot})"
        )


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
