from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from phonenumber_field.modelfields import PhoneNumberField
from .managers import CustomUserManager

class User(AbstractUser):
    username = None
    phone_number = PhoneNumberField(region="IR", unique=True)
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = CustomUserManager()
    def __str__(self):
        return self.phone_number.__str__()




