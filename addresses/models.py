from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model

User = get_user_model()

class Province(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("استان"),
    )

    class Meta:
        verbose_name = _("استان")
        verbose_name_plural = _("استان‌ها")
        ordering = ["name"]

    def __str__(self):
        return self.name


class City(models.Model):
    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        related_name="cities",
        verbose_name=_("استان"),
    )

    name = models.CharField(
        max_length=100,
        verbose_name=_("شهر"),
    )

    class Meta:
        verbose_name = _("شهر")
        verbose_name_plural = _("شهرها")
        ordering = ["name"]

        constraints = [
            models.UniqueConstraint(
                fields=["province", "name"],
                name="unique_city_per_province",
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.province.name}"



class Address(models.Model):

    class AddressType(models.TextChoices):
        HOME = "home", _("خانه")
        WORK = "work", _("محل کار")
        OTHER = "other", _("سایر")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="addresses",
        verbose_name=_("کاربر"),
    )

    title = models.CharField(
        max_length=100,
        verbose_name=_("عنوان"),
        help_text=_("مثال: خانه، محل کار"),
    )

    address_type = models.CharField(
        max_length=20,
        choices=AddressType.choices,
        default=AddressType.HOME,
        verbose_name=_("نوع آدرس"),
    )

    receiver_name = models.CharField(
        max_length=150,
        verbose_name=_("نام گیرنده"),
    )

    receiver_phone = PhoneNumberField(
        region="IR",
        verbose_name=_("شماره تماس گیرنده"),
        db_index=False
    )

    province = models.ForeignKey(
        Province,
        on_delete=models.PROTECT,
        related_name="addresses",
        verbose_name=_("استان"),
    )

    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        related_name="addresses",
        verbose_name=_("شهر"),
    )

    address_line = models.TextField(
        verbose_name=_("آدرس"),
    )

    alley = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("کوچه"),
    )

    plaque = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("پلاک"),
    )

    unit = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("واحد"),
    )

    postal_code = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r"^\d{10}$",
                message=_("کد پستی باید ۱۰ رقم باشد."),
            )
        ],
        verbose_name=_("کد پستی"),
    )

    description = models.TextField(
        blank=True,
        verbose_name=_("توضیحات"),
        help_text=_("توضیحات لازم برای تحویل سفارش"),
    )

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True,
        verbose_name=_("عرض جغرافیایی"),
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True,
        verbose_name=_("طول جغرافیایی"),
    )

    is_default = models.BooleanField(
        default=False,
        verbose_name=_("آدرس پیش‌فرض"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("تاریخ ایجاد"),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("تاریخ بروزرسانی"),
    )

    delivery_note = models.TextField(
        blank=True,
        verbose_name=_("راهنمای تحویل"),
    )

    class Meta:
        verbose_name = _("آدرس")
        verbose_name_plural = _("آدرس‌ها")

        ordering = ["-is_default", "-created_at"]

        indexes = [
            models.Index(
                fields=["user"],
                name="address_user_idx",
            ),
            models.Index(
                fields=["province", "city"],
                name="address_location_idx",
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                condition=Q(is_default=True),
                name="unique_default_address_per_user",
            ),
        ]

    def __str__(self):
        return f"{self.title} - {self.receiver_name}"
