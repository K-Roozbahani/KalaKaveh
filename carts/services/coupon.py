from django.utils import timezone

from discounts.models import Coupon


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