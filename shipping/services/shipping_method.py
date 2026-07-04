from shipping.selectors import get_active_shipping_methods


def get_available_shipping_methods(

    *,

    cart,

    address,

):
    """
    برگرداندن روش‌های ارسال قابل استفاده برای سفارش.

    در نسخه فعلی فقط روش‌های ارسال فعال برگردانده می‌شوند.

    در آینده قوانین مربوط به شهر، وزن، ابعاد، کلاس حمل،
    ارسال رایگان و سایر محدودیت‌ها در همین Service
    اعمال خواهند شد.
    """

    return get_active_shipping_methods().order_by("price", "id")