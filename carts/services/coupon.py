from django.utils import timezone

from discounts.models import Coupon

from carts.models import Cart


def apply_coupon(
    *,
    cart,
    code,
):
    """
    اعمال کد تخفیف
    """

    coupon = Coupon.objects.get(
        code=code
    )

    # اعتبارسنجی کامل
    # فعال بودن
    # تاریخ اعتبار
    # تعداد استفاده

    cart.coupon = coupon

    cart.save(
        update_fields=["coupon"]
    )

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