from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _


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