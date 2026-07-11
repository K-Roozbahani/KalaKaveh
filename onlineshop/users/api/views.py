from .serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from utils.permissions import IsOwnerOrAdmin
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.network import get_client_ip

from users.api.serializers import (
    RequestOTPSerializer,
    VerifyOTPSerializer,
)
from users.services.authentication import (
    authenticate_by_otp,
    request_otp,
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
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated()]

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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate_by_otp(
            phone_number=serializer.validated_data["phone_number"],
            otp=serializer.validated_data["otp"],
            ip_address=get_client_ip(request),
        )

        return Response(
            {
                "user_id": user.id,
            },
            status=status.HTTP_200_OK,
        )