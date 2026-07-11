from django.core.cache import cache

from users.constants import (
    RATE_LIMITS,
    REDIS_KEY_RATE_LIMIT,
)
from users.exceptions import RateLimitExceededException


def check_rate_limit(
    *,
    action: str,
    identifier: str,
) -> None:
    """
    بررسی محدودیت تعداد درخواست‌ها.

    Args:
        action: نام عملیات (مانند otp_request).
        identifier: شناسه محدودسازی (شماره موبایل، IP و ...).

    Raises:
        RateLimitExceededException:
            در صورت عبور از محدودیت.
    """

    limits = RATE_LIMITS.get(action)

    if not limits:
        return

    for config in limits:
        redis_key = REDIS_KEY_RATE_LIMIT.format(
            action=action,
            identifier=identifier,
            period=config["name"],
        )

        counter = cache.get(redis_key, 0)

        if counter >= config["limit"]:
            raise RateLimitExceededException

        if counter == 0:
            cache.set(
                redis_key,
                1,
                timeout=config["window"],
            )
        else:
            cache.incr(redis_key)