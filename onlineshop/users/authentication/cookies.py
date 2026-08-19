"""
ابزارهای مدیریت Cookieهای مربوط به احراز هویت JWT.
"""

from django.conf import settings
from django.http import HttpResponse


def set_auth_cookies(
    response: HttpResponse,
    access_token: str,
    refresh_token: str,
) -> HttpResponse:
    """
    Access Token و Refresh Token را در Cookieهای امن قرار می‌دهد.
    """

    access_lifetime = settings.SIMPLE_JWT[
        "ACCESS_TOKEN_LIFETIME"
    ]

    refresh_lifetime = settings.SIMPLE_JWT[
        "REFRESH_TOKEN_LIFETIME"
    ]

    response.set_cookie(
        key=settings.AUTH_COOKIE_ACCESS,
        value=access_token,
        max_age=int(access_lifetime.total_seconds()),
        httponly=True,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite=settings.AUTH_COOKIE_SAMESITE,
        path="/",
    )

    response.set_cookie(
        key=settings.AUTH_COOKIE_REFRESH,
        value=refresh_token,
        max_age=int(refresh_lifetime.total_seconds()),
        httponly=True,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite=settings.AUTH_COOKIE_SAMESITE,
        path="Path=/api/user/auth/",
    )

    return response