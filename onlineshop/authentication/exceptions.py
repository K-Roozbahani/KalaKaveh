from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import APIException
from rest_framework import status


# ===========================================================
# Base Authentication Exception
# ===========================================================

class AuthenticationException(APIException):
    """
    کلاس پایه خطاهای احراز هویت.
    """

    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "authentication_error"
    default_detail = _("خطا در احراز هویت.")


# ===========================================================
# OTP Exceptions
# ===========================================================

class InvalidOTPException(AuthenticationException):
    """
    کد یکبار مصرف نامعتبر است.
    """

    default_code = "invalid_otp"
    default_detail = _("کد تایید نامعتبر است.")


class OTPExpiredException(AuthenticationException):
    """
    کد یکبار مصرف منقضی شده است.
    """

    default_code = "otp_expired"
    default_detail = _("کد تایید منقضی شده است.")


# ===========================================================
# Blacklist Exceptions
# ===========================================================

class PhoneNumberBlockedException(AuthenticationException):
    """
    شماره موبایل در لیست سیاه قرار دارد.
    """

    status_code = status.HTTP_403_FORBIDDEN
    default_code = "phone_number_blocked"
    default_detail = _("دسترسی این شماره موبایل مسدود شده است.")


class IPAddressBlockedException(AuthenticationException):
    """
    آدرس IP در لیست سیاه قرار دارد.
    """

    status_code = status.HTTP_403_FORBIDDEN
    default_code = "ip_address_blocked"
    default_detail = _("دسترسی این آدرس IP مسدود شده است.")


class RateLimitExceededException(AuthenticationException):
    """
    تعداد درخواست‌های مجاز به پایان رسیده است.
    """

    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_code = "rate_limit_exceeded"
    default_detail = _(
        "تعداد درخواست‌های مجاز به پایان رسیده است. لطفاً بعداً دوباره تلاش کنید."
    )