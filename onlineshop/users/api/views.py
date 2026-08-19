from .serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from utils.permissions import IsOwnerOrAdmin
from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError

from utils.network import get_client_ip

from users.api.serializers import (
    RequestOTPSerializer,
    VerifyOTPSerializer,
)
from users.services.authentication import (
    authenticate_by_otp,
    request_otp,
)
from users.authentication.cookies import (
    set_auth_cookies,
    delete_auth_cookies,
)

User = get_user_model() # این خط مدل سفارشی شما را به درستی پیدا می‌کند

class UserApiView(ModelViewSet):
    lookup_field = 'phone_number'
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            # اینجا چون داریم لیست رو برمیکردونیم باید از () استفاده شود
            return [AllowAny(),]


        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

        elif self.action == 'list':
            self.permission_classes = [IsAdminUser,]
        else:
            self.permission_classes = [IsAuthenticated,]

        return super().get_permissions()


class AuthenticationViewSet(GenericViewSet):
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request_otp(
            phone_number=serializer.validated_data["phone_number"],
            ip_address=get_client_ip(request),
        )

        return Response(
            {"detail": "کد تأیید ارسال شد."},
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

        پس از تأیید موفق OTP، توکن‌های JWT ایجاد شده و
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