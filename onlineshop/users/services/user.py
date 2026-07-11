from django.db import transaction

from phonenumber_field.phonenumber import PhoneNumber

from users.models import User


@transaction.atomic
def get_or_create_user_by_phone(
    *,
    phone_number: PhoneNumber,
) -> User:
    """
    دریافت یا ایجاد کاربر بر اساس شماره موبایل.
    """

    user, _ = User.objects.get_or_create(
        phone_number=phone_number,
    )

    return user