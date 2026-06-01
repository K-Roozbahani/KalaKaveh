from ..models import User
from .serializer import UserSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from utils.permissions import IsOwnerOrAdmin

class UserApiView(ModelViewSet):
    lookup_field = 'phone_number'
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        print("**************************step main*******************")
        if self.action == 'create':
            # اینجا چون داریم لیست رو برمیکردونیم باید از () استفاده شود
            return [AllowAny()]


        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            #جایی که از داریم کلاس معرفی میکنیم نباید () استفاده شود وگرنه خطا میگیرد
            print("**************************step update, others*******************")
            self.permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

        elif self.action == 'list':
            print("**************************step list*******************")
            self.permission_classes = [IsAdminUser]
        else:
            print("**************************step else*******************")
            self.permission_classes = [IsAuthenticated()]
        print("**************************step skip all*******************")
        return super().get_permissions()