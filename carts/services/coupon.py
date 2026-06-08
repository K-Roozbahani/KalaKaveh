from django.utils import timezone

from discounts.models import Coupon

from carts.models import Cart

from rest_framework.exceptions import ValidationError


def validate_coupon(*, cart, code):
    """
    اعتبارسنجی کد تخفیف.
    """

    try:
        coupon = Coupon.objects.select_related("discount").get(
            code=code,
        )

    except Coupon.DoesNotExist:
        raise ValidationError(
            {
                "code": "کد تخفیف معتبر نیست."
            }
        )

    now = timezone.now()

    discount = coupon.discount

    if not discount.is_active:
        raise ValidationError(
            {
                "code": "کد تخفیف غیرفعال است."
            }
        )

    if discount.start_date and discount.start_date > now:
        raise ValidationError(
            {
                "code": "زمان استفاده از این کد تخفیف هنوز آغاز نشده است."
            }
        )

    if discount.end_date and discount.end_date < now:
        raise ValidationError(
            {
                "code": "اعتبار کد تخفیف به پایان رسیده است."
            }
        )

    if (
        coupon.usage_limit
        and coupon.used_count >= coupon.usage_limit
    ):
        raise ValidationError(
            {
                "code": "ظرفیت استفاده از این کد تخفیف تکمیل شده است."
            }
        )

    return coupon


def apply_coupon(
    *,
    cart,
    code,
):
    """
    اعمال کد تخفیف
    """

    coupon = validate_coupon(code=code)

    cart.coupon = coupon

    cart.save(update_fields=["coupon"])

    return cart


def remove_coupon(*, cart: Cart):
    """
    حذف کوپن از سبد خرید.
    """

    if not cart.coupon_id:
        return

    cart.coupon = None

    cart.save(update_fields=["coupon"])

    return cart


