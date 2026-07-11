import logging

logger = logging.getLogger("authentication")


def send_otp(
    *,
    phone_number: str,
    otp: str,
) -> None:
    """
    ارسال کد یکبار مصرف.

    در محیط توسعه، کد تأیید فقط در لاگ ثبت می‌شود.
    """

    logger.info(
        "OTP | phone_number=%s | otp=%s",
        phone_number,
        otp,
    )
    print(f"OTP | {phone_number} | {otp}")