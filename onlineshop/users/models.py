from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField
from .managers import CustomUserManager

class User(AbstractUser):
    username = None
    phone_number = PhoneNumberField(region="IR", unique=True, verbose_name="شماره تلفن", help_text="شماره تماس مثل: 09120000000")

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = CustomUserManager()
    def __str__(self):
        return self.phone_number.__str__()


class Blacklist(models.Model):
    """
    لیست سیاه برای جلوگیری از ارسال OTP و درخواست‌های نامعتبر.
    """

    phone_number = PhoneNumberField(
        region="IR",
        blank=True,
        null=True,
        verbose_name=_("شماره موبایل"),
    )

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        verbose_name=_("آدرس IP"),
    )

    reason = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("دلیل"),
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("فعال"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("زمان ایجاد"),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("زمان بروزرسانی"),
    )

    class Meta:
        verbose_name = _("لیست سیاه")
        verbose_name_plural = _("لیست سیاه")

    def __str__(self):
        return self.phone_number or self.ip_address