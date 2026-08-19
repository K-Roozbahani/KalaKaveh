"""
احراز هویت JWT مبتنی بر Cookie.

Access Token از Cookie دریافت می‌شود و اعتبارسنجی آن
توسط مکانیزم استاندارد Simple JWT انجام می‌گیرد.
"""

from django.conf import settings

from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    """
    احراز هویت کاربران با استفاده از Access Token موجود در Cookie.
    """

    def authenticate(self, request):
        """
        Access Token را از Cookie دریافت و اعتبارسنجی می‌کند.
        """

        raw_token = request.COOKIES.get(
            settings.AUTH_COOKIE_ACCESS,
        )

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(
            raw_token,
        )

        return (
            self.get_user(validated_token),
            validated_token,
        )