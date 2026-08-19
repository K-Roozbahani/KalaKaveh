from secrets import randbelow

from django.core.cache import cache

from users.constants import (
    OTP_LENGTH,
    OTP_TTL,
    REDIS_KEY_OTP,
)
from users.exceptions import (
    InvalidOTPException,
    OTPExpiredException,
)


# ===========================================================
# OTP Services
# ===========================================================

def generate_otp() -> str:
    """
    تولید کد یکبار مصرف.
    """
    minimum = 10 ** (OTP_LENGTH - 1)
    maximum = 10 ** OTP_LENGTH

    return str(minimum + randbelow(maximum - minimum))


def save_otp(
    *,
    phone_number: str,
    otp: str,
) -> None:
    """
    ذخیره کد یکبار مصرف در Redis.
    """
    cache.set(
        REDIS_KEY_OTP.format(phone=phone_number),
        otp,
        timeout=OTP_TTL,
    )


def get_otp(
    *,
    phone_number: str,
) -> str | None:
    """
    دریافت کد یکبار مصرف از Redis.
    """
    return cache.get(
        REDIS_KEY_OTP.format(phone=phone_number),
    )


def delete_otp(
    *,
    phone_number: str,
) -> None:
    """
    حذف کد یکبار مصرف از Redis.
    """
    cache.delete(
        REDIS_KEY_OTP.format(phone=phone_number),
    )


def verify_otp(
    *,
    phone_number: str,
    otp: str,
) -> None:
    """
    اعتبارسنجی کد یکبار مصرف.
    """

    cached_otp = get_otp(
        phone_number=phone_number,
    )

    if cached_otp is None:
        raise OTPExpiredException

    if cached_otp != otp:
        raise InvalidOTPException

    delete_otp(
        phone_number=phone_number,
    )