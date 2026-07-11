from phonenumber_field.phonenumber import PhoneNumber

from users.constants import (
    RATE_LIMIT_ACTION_OTP_REQUEST,
    RATE_LIMIT_ACTION_OTP_VERIFY,
)

from users.services.otp import (
    generate_otp,
    save_otp,
    verify_otp,
)

from users.services.rate_limit import check_rate_limit
from users.services.request_validation import validate_request_source
from users.services.sms import send_otp
from users.services.user import get_or_create_user_by_phone


def request_otp(
    *,
    phone_number: PhoneNumber,
    ip_address: str,
) -> None:
    """
    ایجاد و ارسال کد یکبار مصرف.
    """

    validate_request_source(
        phone_number=phone_number,
        ip_address=ip_address,
    )

    check_rate_limit(
        action=RATE_LIMIT_ACTION_OTP_REQUEST,
        identifier=str(phone_number),
    )

    otp = generate_otp()

    save_otp(
        phone_number=str(phone_number),
        otp=otp,
    )

    send_otp(
        phone_number=str(phone_number),
        otp=otp,
    )


def authenticate_by_otp(
    *,
    phone_number: PhoneNumber,
    otp: str,
    ip_address: str,
):
    """
    احراز هویت کاربر با کد یکبار مصرف.
    """

    validate_request_source(
        phone_number=phone_number,
        ip_address=ip_address,
    )

    check_rate_limit(
        action=RATE_LIMIT_ACTION_OTP_VERIFY,
        identifier=str(phone_number),
    )

    verify_otp(
        phone_number=str(phone_number),
        otp=otp,
    )

    return get_or_create_user_by_phone(
        phone_number=phone_number,
    )