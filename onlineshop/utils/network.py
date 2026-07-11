from django.http import HttpRequest


def get_client_ip(
    request: HttpRequest,
) -> str:
    """
    دریافت IP واقعی کاربر.

    در صورت وجود Reverse Proxy از X-Forwarded-For
    استفاده می‌شود، در غیر این صورت REMOTE_ADDR
    برگردانده خواهد شد.
    """

    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR", "")