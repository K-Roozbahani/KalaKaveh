from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from phonenumber_field.modelfields import PhoneNumberField
from .managers import CustomUserManager

class User(AbstractUser):
    username = None
    phone_number = PhoneNumberField(region="IR", unique=True, verbose_name="شماره تلفن", help_text="شماره تماس مثل: 09120000000")

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = CustomUserManager()
    def __str__(self):
        return self.phone_number.__str__()


from django.db import models
from django.contrib.auth.models import User


class Address(models.Model):
    # اتصال به کاربر؛ حذف شدن کاربر، آدرس‌های او را هم پاک می‌کند
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')

    # جزئیات آدرس
    title = models.CharField(max_length=50, help_text="عنوان آدرس مثل: خانه یا محل کار")
    state = models.CharField(max_length=50, help_text="استان")
    city = models.CharField(max_length=50, help_text="شهر")
    street = models.CharField(max_length=255, help_text="نام خیابان و کوچه")
    postal_code = models.CharField(max_length=10, help_text="کد پستی")
    phone_number = models.CharField(max_length=15, help_text="شماره تماس مرتبط با این آدرس")

    # فیلد برای ذخیره جزئیات بیشتر مثل واحد یا پلاک
    address_details = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس‌ها"

    def __str__(self):
        return f"{self.title} - {self.city}"




