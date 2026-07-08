from django.contrib.auth.models import AbstractUser
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