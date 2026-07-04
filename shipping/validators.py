from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _

from shipping.models import ShippingMethod


def validate_shipping_method_exists(
    shipping_method,
):
    if shipping_method is None:
        raise ValidationError(
            _("روش ارسال یافت نشد.")
        )


def validate_shipping_method_active(
    shipping_method,
):
    if not shipping_method.is_active:
        raise ValidationError(
            _("روش ارسال غیرفعال است.")
        )


def validate_shipment_exists(
    shipment,
):
    if shipment is None:
        raise ValidationError(
            _("مرسوله یافت نشد.")
        )

def validate_shipping_method_available(
    *,
    shipping_method: ShippingMethod,
    available_shipping_methods,
) -> None:
    """
    بررسی می‌کند که روش ارسال انتخاب‌شده
    در لیست روش‌های قابل استفاده برای سفارش باشد.
    """

    if shipping_method not in available_shipping_methods:
        raise ValidationError(
            _("روش ارسال انتخواب شده در لیست روش های قابل انتخواب نیست.")
        )