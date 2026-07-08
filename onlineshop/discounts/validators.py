from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from discounts.models import (
    Discount,
    Coupon,
)


def validate_discount_date_range(
    *,
    start_date,
    end_date,
) -> None:
    """
    اعتبارسنجی بازه زمانی تخفیف
    """

    if start_date >= end_date:
        raise ValidationError(
            _("تاریخ پایان باید بعد از تاریخ شروع باشد.")
        )


def validate_discount_is_active(
    *,
    discount: Discount,
) -> None:
    """
    بررسی فعال بودن تخفیف
    """

    now = timezone.now()

    if not discount.is_active:
        raise ValidationError(
            _("تخفیف غیرفعال است.")
        )

    if discount.start_date > now:
        raise ValidationError(
            _("تخفیف هنوز فعال نشده است.")
        )

    if discount.end_date < now:
        raise ValidationError(
            _("تخفیف منقضی شده است.")
        )

def validate_coupon_is_active(
    *,
    coupon: Coupon,
) -> None:
    """
    بررسی فعال بودن کوپن
    """

    now = timezone.now()

    if not coupon.is_active:
        raise ValidationError(
            _("کوپن غیرفعال است.")
        )

    if coupon.start_date > now:
        raise ValidationError(
            _("کوپن هنوز فعال نشده است.")
        )

    if coupon.end_date < now:
        raise ValidationError(
            _("کوپن منقضی شده است.")
        )


def validate_coupon_date_range(
    *,
    start_date,
    end_date,
) -> None:
    """
    اعتبارسنجی بازه زمانی کوپن
    """

    if start_date >= end_date:
        raise ValidationError(
            _("تاریخ پایان باید بعد از تاریخ شروع باشد.")
        )


def validate_coupon_usage_limit(
    *,
    coupon: Coupon,
) -> None:
    """
    بررسی ظرفیت مصرف کوپن
    """

    if coupon.used_count >= coupon.usage_limit:
        raise ValidationError(
            _("ظرفیت استفاده از این کوپن تکمیل شده است.")
        )


def validate_user_has_not_used_coupon(
    *,
    has_used: bool,
) -> None:
    """
    جلوگیری از استفاده مجدد کاربر
    """

    if has_used:
        raise ValidationError(
            _("شما قبلاً از این کوپن استفاده کرده‌اید.")
        )



def validate_price(
    *,
    price: int,
) -> None:
    """
    اعتبارسنجی قیمت
    """

    if price < 0:
        raise ValidationError(
            _("قیمت نمی‌تواند منفی باشد.")
        )


def validate_discount_amount(
    *,
    discount_amount: int,
    price: int,
) -> None:
    """
    اعتبارسنجی مبلغ تخفیف
    """

    if discount_amount < 0:
        raise ValidationError(
            _("مبلغ تخفیف نامعتبر است.")
        )

    if discount_amount > price:
        raise ValidationError(
            _("مبلغ تخفیف نمی‌تواند بیشتر از قیمت باشد.")
        )


def validate_final_price(
    *,
    final_price: int,
) -> None:
    """
    اعتبارسنجی قیمت نهایی
    """

    if final_price < 0:
        raise ValidationError(
            _("قیمت نهایی نمی‌تواند منفی باشد.")
        )


