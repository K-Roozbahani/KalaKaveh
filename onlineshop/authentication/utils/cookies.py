"""
ابزارهای مدیریت Cookieهای مربوط به احراز هویت JWT.

Cookieهای Access و Refresh به صورت HttpOnly ذخیره می‌شوند
تا JavaScript سمت Frontend امکان دسترسی مستقیم به Tokenها را نداشته باشد.
"""

from django.conf import settings
from django.http import HttpResponse


def set_auth_cookies(
    response: HttpResponse,
    access_token: str,
    refresh_token: str,
) -> HttpResponse:
    """
    ذخیره Access Token و Refresh Token در Cookieهای امن.

    Access Token:
        برای تمام APIها قابل ارسال است.

    Refresh Token:
        فقط برای Endpointهای Authentication ارسال می‌شود.
    """

    access_lifetime = settings.SIMPLE_JWT[
        "ACCESS_TOKEN_LIFETIME"
    ]

    refresh_lifetime = settings.SIMPLE_JWT[
        "REFRESH_TOKEN_LIFETIME"
    ]

    # ------------------------------------------------------
    # Access Token Cookie
    # ------------------------------------------------------

    response.set_cookie(
        key=settings.AUTH_COOKIE_ACCESS,
        value=access_token,
        max_age=int(
            access_lifetime.total_seconds(),
        ),
        httponly=True,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite=settings.AUTH_COOKIE_SAMESITE,
        path="/",
    )

    # ------------------------------------------------------
    # Refresh Token Cookie
    # ------------------------------------------------------

    response.set_cookie(
        key=settings.AUTH_COOKIE_REFRESH,
        value=refresh_token,
        max_age=int(
            refresh_lifetime.total_seconds(),
        ),
        httponly=True,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite=settings.AUTH_COOKIE_SAMESITE,
        path="/",
    )

    return response


def delete_auth_cookies(
    response: HttpResponse,
) -> HttpResponse:
    """
    حذف Cookieهای مربوط به احراز هویت.
    """

    response.delete_cookie(
        key=settings.AUTH_COOKIE_ACCESS,
        path="/",
    )

    response.delete_cookie(
        key=settings.AUTH_COOKIE_REFRESH,
        path="/",
    )

    return response