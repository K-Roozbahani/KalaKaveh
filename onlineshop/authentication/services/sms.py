from django.conf import settings

from sms_ir import SmsIr


class SMSProviderError(Exception):
    """خطا در ارتباط با سرویس پیامک."""


class SMSIRService:
    """ارسال پیامک OTP از طریق SMS.ir."""

    def __init__(self):
        self.client = SmsIr(
            settings.SMSIR["API_KEY"],
            settings.SMSIR["LINE_NUMBER"],
        )

    def send_otp(self, phone_number: str, code: str):
        try:
            return self.client.send_verify_code(
                number=int(phone_number),
                template_id=settings.SMSIR["OTP_TEMPLATE_ID"],
                parameters=[
                    {
                        "name": "CODE",
                        "value": str(code),
                    }
                ],
            )
        except Exception as exc:
            raise SMSProviderError(
                "Failed to send OTP through SMS.ir."
            ) from exc


import logging
logger = logging.getLogger("authentication")


def send_otp(
    *,
    phone_number: str,
    code: str,
) -> None:
    """
ارسال کد یکبار مصرف
در محیط توسعه، کد تأیید فقط در لاگ ثبت می‌شود.
"""

    logger.info(
        "OTP | phone_number=%s | otp=%s",
        phone_number,
        code,
    )
    print(f"OTP | {phone_number} | {code}")