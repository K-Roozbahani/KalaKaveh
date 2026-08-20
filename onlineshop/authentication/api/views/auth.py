from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.api.serializers import (
    RequestOTPSerializer,
    VerifyOTPSerializer,
)
from authentication.services.authentication import (
    authenticate_by_otp,
    request_otp,
)
from authentication.utils.cookies import (
    delete_auth_cookies,
    set_auth_cookies,
)

from utils.api.views import BaseGenericViewSet
from utils.network import get_client_ip


User = get_user_model()


@extend_schema_view(
    request_otp=extend_schema(
        summary="درخواست کد OTP",
        description=(
            "ارسال کد OTP برای شماره تلفن کاربر. "
            "این Endpoint نیاز به احراز هویت ندارد، "
            "اما به دلیل استفاده از Cookie Authentication "
            "تحت محافظت CSRF قرار دارد."
        ),
        request=RequestOTPSerializer,
        responses={
            200: OpenApiResponse(
                description="کد تأیید با موفقیت ارسال شد.",
            ),
            400: OpenApiResponse(
                description="اطلاعات ارسال‌شده معتبر نیست.",
            ),
            403: OpenApiResponse(
                description="CSRF Token نامعتبر یا ارسال نشده است.",
            ),
        },
        tags=["Authentication"],
    ),
    verify_otp=extend_schema(
        summary="تأیید OTP و ورود",
        description=(
            "کد OTP را تأیید کرده و پس از ورود موفق، "
            "Access Token و Refresh Token را به صورت "
            "HttpOnly Cookie در Response قرار می‌دهد."
        ),
        request=VerifyOTPSerializer,
        responses={
            200: OpenApiResponse(
                description="ورود با موفقیت انجام شد و Cookieهای احراز هویت تنظیم شدند.",
            ),
            400: OpenApiResponse(
                description="کد OTP نامعتبر یا منقضی شده است.",
            ),
            403: OpenApiResponse(
                description="CSRF Token نامعتبر یا ارسال نشده است.",
            ),
        },
        tags=["Authentication"],
    ),
    refresh=extend_schema(
        summary="به‌روزرسانی Access Token",
        description=(
            "Refresh Token از HttpOnly Cookie دریافت شده و "
            "Access Token جدید صادر می‌شود. "
            "در صورت فعال بودن Rotation، Refresh Token جدید "
            "نیز صادر خواهد شد."
        ),
        request=None,
        responses={
            200: OpenApiResponse(
                description="Tokenها با موفقیت به‌روزرسانی شدند.",
            ),
            401: OpenApiResponse(
                description="Refresh Token وجود ندارد، منقضی شده یا نامعتبر است.",
            ),
            403: OpenApiResponse(
                description="CSRF Token نامعتبر یا ارسال نشده است.",
            ),
        },
        tags=["Authentication"],
    ),
    logout=extend_schema(
        summary="خروج از حساب کاربری",
        description=(
            "Refresh Token موجود در HttpOnly Cookie را "
            "Blacklist کرده و Cookieهای احراز هویت را حذف می‌کند."
        ),
        request=None,
        responses={
            200: OpenApiResponse(
                description="کاربر با موفقیت خارج شد.",
            ),
            403: OpenApiResponse(
                description="CSRF Token نامعتبر یا ارسال نشده است.",
            ),
        },
        tags=["Authentication"],
    ),
)
class AuthenticationViewSet(BaseGenericViewSet):
    """
    عملیات احراز هویت کاربران.
    """

    permission_classes = (AllowAny,)

    @action(
        detail=False,
        methods=["post"],
        serializer_class=RequestOTPSerializer,
        url_path="request-otp",
    )
    def request_otp(self, request):
        """
        ارسال کد OTP برای شماره تلفن کاربر.
        """

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        request_otp(
            phone_number=serializer.validated_data["phone_number"],
            ip_address=get_client_ip(request),
        )

        return Response(
            {
                "detail": "کد تأیید ارسال شد.",
            },
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=["post"],
        serializer_class=VerifyOTPSerializer,
        url_path="verify-otp",
    )
    def verify_otp(self, request):
        """
        تأیید کد OTP و ورود کاربر.

        پس از تأیید موفق OTP، توکن‌های JWT
        به صورت HttpOnly Cookie در Response قرار می‌گیرند.
        """

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user = authenticate_by_otp(
            phone_number=serializer.validated_data["phone_number"],
            otp=serializer.validated_data["otp"],
            ip_address=get_client_ip(request),
        )

        refresh = RefreshToken.for_user(user)

        response = Response(
            {
                "user_id": user.id,
            },
            status=status.HTTP_200_OK,
        )

        set_auth_cookies(
            response=response,
            access_token=str(refresh.access_token),
            refresh_token=str(refresh),
        )

        return response

    @action(
        detail=False,
        methods=["post"],
        serializer_class=TokenRefreshSerializer,
        url_path="refresh",
    )
    def refresh(self, request):
        """
        دریافت Refresh Token از Cookie و صدور Tokenهای جدید.

        در صورت فعال بودن Rotation در Simple JWT،
        Refresh Token قبلی Blacklist شده و Refresh Token
        جدید صادر می‌شود.
        """

        refresh_token = request.COOKIES.get(
            settings.AUTH_COOKIE_REFRESH,
        )

        if not refresh_token:
            return Response(
                {
                    "detail": "Refresh Token یافت نشد.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = self.get_serializer(
            data={
                "refresh": refresh_token,
            },
        )

        serializer.is_valid(
            raise_exception=True,
        )

        response = Response(
            {
                "detail": "توکن با موفقیت به‌روزرسانی شد.",
            },
            status=status.HTTP_200_OK,
        )

        set_auth_cookies(
            response=response,
            access_token=serializer.validated_data["access"],
            refresh_token=serializer.validated_data.get(
                "refresh",
                refresh_token,
            ),
        )

        return response

    @action(
        detail=False,
        methods=["post"],
        serializer_class=None,
        url_path="logout",
    )
    def logout(self, request):
        """
        خروج کاربر.

        Refresh Token موجود در Cookie را Blacklist کرده
        و سپس Cookieهای احراز هویت را حذف می‌کند.
        """

        refresh_token = request.COOKIES.get(
            settings.AUTH_COOKIE_REFRESH,
        )

        if refresh_token:
            try:
                token = RefreshToken(
                    refresh_token,
                )

                token.blacklist()

            except TokenError:
                # اگر Token قبلاً منقضی یا Blacklist شده باشد،
                # Logout همچنان باید موفقیت‌آمیز باشد.
                pass

        response = Response(
            {
                "detail": "با موفقیت خارج شدید.",
            },
            status=status.HTTP_200_OK,
        )

        delete_auth_cookies(response)

        return response