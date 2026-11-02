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

    def send_otp(self, phone_number: int, code: str):
        try:
            return self.client.send_verify_code(
                number=phone_number,
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