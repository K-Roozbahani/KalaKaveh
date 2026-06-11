from .serializer import UserSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from utils.permissions import IsOwnerOrAdmin
from django.contrib.auth import get_user_model

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