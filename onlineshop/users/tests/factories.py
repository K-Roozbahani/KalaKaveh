from phonenumber_field.phonenumber import PhoneNumber

from users.models import (
    Blacklist,
    User,
)


def create_user(
    *,
    phone_number: str = "09120000000",
    **kwargs,
) -> User:
    """
    ایجاد کاربر برای تست.
    """

    defaults = {
        "phone_number": PhoneNumber.from_string(
            phone_number=phone_number,
            region="IR",
        ),
    }

    defaults.update(kwargs)

    return User.objects.create(**defaults)


def create_blacklist(
    *,
    phone_number: str | None = None,
    ip_address: str | None = None,
    is_active: bool = True,
    **kwargs,
) -> Blacklist:
    """
    ایجاد رکورد بلک لیست برای تست.
    """

    defaults = {
        "phone_number": (
            PhoneNumber.from_string(
                phone_number=phone_number,
                region="IR",
            )
            if phone_number
            else None
        ),
        "ip_address": ip_address,
        "is_active": is_active,
    }

    defaults.update(kwargs)

    return Blacklist.objects.create(**defaults)