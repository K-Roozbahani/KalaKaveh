from phonenumber_field.phonenumber import PhoneNumber

from users.selectors import (
    get_blacklisted_ip,
    get_blacklisted_phone,
)

from authentication.exceptions import (
    PhoneNumberBlockedException,
    IPAddressBlockedException,
)


# ===========================================================
# Phone Number Validators
# ===========================================================

def validate_phone_blacklist(
    phone_number: PhoneNumber,
) -> None:
    """
    بررسی بلاک بودن شماره موبایل.

    Args:
        phone_number: شماره موبایل.

    Raises:
        PhoneNumberBlockedException: در صورت بلاک بودن شماره.
    """
    if get_blacklisted_phone(phone_number):
        raise PhoneNumberBlockedException


# ===========================================================
# IP Address Validators
# ===========================================================

def validate_ip_blacklist(
    ip_address: str,
) -> None:
    """
    بررسی بلاک بودن آدرس IP.

    Args:
        ip_address: آدرس IP.

    Raises:
        IPAddressBlockedException: در صورت بلاک بودن IP.
    """
    if get_blacklisted_ip(ip_address):
        raise IPAddressBlockedException


