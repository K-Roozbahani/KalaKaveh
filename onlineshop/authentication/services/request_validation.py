from phonenumber_field.phonenumber import PhoneNumber

from users.validators import (
    validate_ip_blacklist,
    validate_phone_blacklist,
)


def validate_request_source(
    *,
    phone_number: PhoneNumber | None = None,
    ip_address: str | None = None,
) -> None:
    """
    اعتبارسنجی منبع درخواست.

    این سرویس مسئول بررسی معتبر بودن منبع درخواست قبل از
    شروع فرآیند احراز هویت است.

    Args:
        phone_number: شماره موبایل کاربر.
        ip_address: آدرس IP درخواست.

    Raises:
        PhoneNumberBlockedException:
            در صورت قرار داشتن شماره موبایل در لیست سیاه.

        IPAddressBlockedException:
            در صورت قرار داشتن آدرس IP در لیست سیاه.
    """

    # بررسی شماره موبایل
    if phone_number:
        validate_phone_blacklist(phone_number)

    # بررسی آدرس IP
    if ip_address:
        validate_ip_blacklist(ip_address)