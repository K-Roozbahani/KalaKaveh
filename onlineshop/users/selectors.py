from phonenumber_field.phonenumber import PhoneNumber

from users.models import Blacklist, User


# ===========================================================
# User Selectors
# ===========================================================

def get_user_by_phone(
    phone_number: PhoneNumber,
) -> User | None:
    """
    دریافت کاربر بر اساس شماره موبایل.

    Args:
        phone_number: شماره موبایل.

    Returns:
        کاربر در صورت وجود، در غیر این صورت None.
    """
    return (
        User.objects
        .filter(phone_number=phone_number)
        .first()
    )


# ===========================================================
# Blacklist Selectors
# ===========================================================

def get_blacklisted_phone(
    phone_number: PhoneNumber,
) -> Blacklist | None:
    """
    دریافت شماره موبایل بلاک شده.

    Args:
        phone_number: شماره موبایل.

    Returns:
        رکورد Blacklist در صورت وجود، در غیر این صورت None.
    """
    return (
        Blacklist.objects
        .filter(
            phone_number=phone_number,
            is_active=True,
        )
        .first()
    )


def get_blacklisted_ip(
    ip_address: str,
) -> Blacklist | None:
    """
    دریافت IP بلاک شده.

    Args:
        ip_address: آدرس IP.

    Returns:
        رکورد Blacklist در صورت وجود، در غیر این صورت None.
    """
    return (
        Blacklist.objects
        .filter(
            ip_address=ip_address,
            is_active=True,
        )
        .first()
    )