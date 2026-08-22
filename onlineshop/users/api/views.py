from django.contrib.auth import get_user_model

from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from utils.api.views import BaseModelViewSet
from utils.permissions import IsOwnerOrAdmin

from users.api.schemas import user_api_schema
from users.api.serializers import UserSerializer


User = get_user_model()


@user_api_schema
class UserApiView(BaseModelViewSet):
    """
    ViewSet مدیریت کاربران.
    """

    lookup_field = "phone_number"
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]

        elif self.action in [
            "retrieve",
            "update",
            "partial_update",
            "destroy",
        ]:
            self.permission_classes = [
                IsAuthenticated,
                IsOwnerOrAdmin,
            ]

        elif self.action == "list":
            self.permission_classes = [IsAdminUser]

        else:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()

    @action(
        detail=False,
        methods=["get"],
        url_path="me",
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        """
        دریافت اطلاعات کاربر احراز هویت‌شده فعلی.
        """
        serializer = self.get_serializer(request.user)

        return Response(serializer.data)