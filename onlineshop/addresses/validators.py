from addresses.models import Address

from django.core.exceptions import PermissionDenied


def validate_address_owner(*, user, address: Address) -> None:
    """
    بررسی می‌کند که آدرس متعلق به کاربر باشد.
    """

    if address.user_id != user.id:
        raise PermissionDenied(
            "این آدرس متعلق به کاربر نیست."
        )