from django.db import transaction

from addresses.models import Address


# ----------------------------
# Create Address
# ----------------------------
@transaction.atomic
def create_address(*, user, **validated_data) -> Address:
    """
    ایجاد آدرس جدید برای کاربر
    - اگر اولین آدرس باشد => default می‌شود
    """

    is_first_address = not Address.objects.filter(user=user).exists()

    address = Address.objects.create(
        user=user,
        is_default=is_first_address,
        **validated_data,
    )

    return address


# ----------------------------
# Update Address
# ----------------------------
@transaction.atomic
def update_address(*, address: Address, **validated_data) -> Address:
    """
    بروزرسانی آدرس
    """

    for attr, value in validated_data.items():
        setattr(address, attr, value)

    address.save()

    return address


# ----------------------------
# Delete Address
# ----------------------------
@transaction.atomic
def delete_address(*, address: Address) -> None:
    """
    حذف آدرس
    - اگر آدرس default باشد => یکی دیگر default می‌شود
    """

    user = address.user
    was_default = address.is_default

    address.delete()

    if was_default:
        new_default = (
            Address.objects
            .filter(user=user)
            .order_by("-created_at")
            .first()
        )

        if new_default:
            new_default.is_default = True
            new_default.save(update_fields=["is_default"])


# ----------------------------
# Set Default Address
# ----------------------------
@transaction.atomic
def set_default_address(*, address: Address) -> Address:
    """
    تنظیم آدرس پیش‌فرض
    - فقط یک آدرس default برای هر کاربر
    """

    Address.objects.filter(
        user=address.user,
        is_default=True
    ).update(is_default=False)

    address.is_default = True
    address.save(update_fields=["is_default"])

    return address