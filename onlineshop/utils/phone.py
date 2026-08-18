import phonenumbers


def format_phone_number(phone_number) -> str | None:
    """
    تبدیل شماره تلفن به فرمت ملی ایران بدون فاصله.

    مثال:
        +989194974979 -> 09194974979
    """
    if not phone_number:
        return None

    formatted = phonenumbers.format_number(
        phone_number,
        phonenumbers.PhoneNumberFormat.NATIONAL,
    )

    return formatted.replace(" ", "")