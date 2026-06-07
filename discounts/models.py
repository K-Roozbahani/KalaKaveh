from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator

from products.models import Product, ProductVariant, Category, Brand


class Discount(models.Model):

    PERCENT = "percent"
    FIXED = "fixed"

    TYPE_CHOICES = (
        (PERCENT, _("درصدی")),
        (FIXED, _("مبلغ ثابت")),
    )

    name = models.CharField(
        _("عنوان"),
        max_length=255
    )

    discount_type = models.CharField(
        _("نوع تخفیف"),
        max_length=20,
        choices=TYPE_CHOICES
    )

    value = models.PositiveIntegerField(
        _("مقدار تخفیف"),
        validators=[MaxValueValidator(100)]
    )

    priority = models.PositiveIntegerField(
        default=0
    )

    is_active = models.BooleanField(
        _("فعال"),
        default=True
    )

    start_date = models.DateTimeField(
        _("شروع")
    )

    end_date = models.DateTimeField(
        _("پایان")
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = _("تخفیف")
        verbose_name_plural = _("تخفیف‌ها")

    def __str__(self):
        return self.name


class DiscountTarget(models.Model):

    discount = models.ForeignKey(
        Discount,
        on_delete=models.CASCADE,
        related_name="targets"
    )

    target_type = models.PositiveSmallIntegerField(
        choices=(
            (1, _("برند")),
            (2, _("دسته بندی")),
            (3, _("محصول")),
            (4, _("محصول انتخوابی")),
        )
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def clean(self):
        targets = [
            self.variant,
            self.product,
            self.category,
            self.brand,
        ]

        filled = sum(
            1
            for item in targets
            if item is not None
        )

        if filled != 1:
            raise ValidationError(
                "دقیقاً یکی از فیلدهای variant, product, category, brand باید مقدار داشته باشد."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = _("هدف تخفیف")
        verbose_name_plural = _("اهداف تخفیف")


class Coupon(models.Model):

    code = models.CharField(
        _("کد"),
        max_length=50,
        unique=True
    )

    discount = models.ForeignKey(
        Discount,
        on_delete=models.CASCADE,
        related_name="coupons"
    )

    usage_limit = models.PositiveIntegerField(
        _("حداکثر استفاده"),
        default=1
    )

    used_count = models.PositiveIntegerField(
        _("تعداد استفاده"),
        default=0
    )

    is_active = models.BooleanField(
        _("فعال"),
        default=True
    )

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.code


class CouponUsage(models.Model):

    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.CASCADE,
        related_name="usages"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE
    )

    used_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            "coupon",
            "user"
        )


