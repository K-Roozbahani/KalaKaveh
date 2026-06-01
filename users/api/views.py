from ..models import Address
from .serializer import UserSerializer, AddressSerializer
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

class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsOwnerOrAdmin] # فقط کاربران لاگین شده

    def get_queryset(self):
        # کاربر فقط می‌تواند آدرس‌های متعلق به خودش را مشاهده کند
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # هنگام ذخیره، کاربرِ لاگین شده را به صورت خودکار به آدرس متصل می‌کند
        serializer.save(user=self.request.user)