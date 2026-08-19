# ===========================================================
# OTP Validators
# ===========================================================
from authentication.exceptions import InvalidOTPException


def validate_otp(
    otp: str,
) -> None:
    """
    اعتبارسنجی فرمت کد یکبار مصرف.

    Args:
        otp: کد یکبار مصرف.

    Raises:
        InvalidOTPException: در صورت نامعتبر بودن فرمت کد.
    """
    if not otp.isdigit():
        raise InvalidOTPException

    if len(otp) != 6:
        raise InvalidOTPException