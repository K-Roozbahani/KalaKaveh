from django.utils.translation import gettext_lazy as _

# ===========================================================
# OTP
# ===========================================================

#: تعداد ارقام کد یکبار مصرف
OTP_LENGTH = 6

#: مدت اعتبار کد یکبار مصرف (ثانیه)
OTP_TTL = 120

# Actions
RATE_LIMIT_ACTION_OTP_REQUEST = "otp_request"
RATE_LIMIT_ACTION_OTP_VERIFY = "otp_verify"

# ===========================================================
# Rate Limit
# ===========================================================

RATE_LIMITS = {
    RATE_LIMIT_ACTION_OTP_REQUEST: [
        {
            "name": "minute",
            "window": 60,
            "limit": 1,
        },
        {
            "name": "hour",
            "window": 3600,
            "limit": 5,
        },
        {
            "name": "day",
            "window": 86400,
            "limit": 20,
        },
    ],
    RATE_LIMIT_ACTION_OTP_VERIFY: [
        {
            "name": "minute",
            "window": 300,
            "limit": 5,
        },
        {
            "name": "day",
            "window": 86400,
            "limit": 20,
        },
    ],
}


# ===========================================================
# Temporary Block
# ===========================================================

#: مدت زمان بلاک موقت (ثانیه)
TEMPORARY_BLOCK_TTL = 3600


# ===========================================================
# Redis Keys
# ===========================================================

#: otp:09121234567
REDIS_KEY_OTP = "otp:{phone}"

#: rate_limit:otp_request:09121234567:minute
REDIS_KEY_RATE_LIMIT = (
    "rate_limit:{action}:{identifier}:{period}"
)

#: block:09121234567
REDIS_KEY_BLOCK = "block:{identifier}"


# ===========================================================
# OTP Log
# ===========================================================

#: تعداد روزهای نگهداری لاگ OTP
OTP_LOG_RETENTION_DAYS = 30