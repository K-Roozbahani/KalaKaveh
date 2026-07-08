from rest_framework import serializers
from ..models import User
from phonenumber_field.serializerfields import PhoneNumberField

class UserSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(region='IR')
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'first_name', 'last_name', 'password')
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        # اگر نیاز به آپدیت دارید، منطق آن را اینجا اضافه کنید
        # معمولاً رمز عبور را مستقیماً آپدیت نمی‌کنیم مگر اینکه منطق خاصی داشته باشیم
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        # برای آپدیت رمز عبور، از متد set_password استفاده کنید
        # password = validated_data.get('password')
        # if password:
        #     instance.set_password(password)
        instance.save()
        return instance