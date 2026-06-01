from django.contrib import admin
from django.contrib.auth import get_user_model
# Register your models here.

class AdminUser(admin.ModelAdmin):
    fields = ("first_name", "last_name", "phone_number", "email", "last_login")
admin.site.register(get_user_model(), AdminUser)