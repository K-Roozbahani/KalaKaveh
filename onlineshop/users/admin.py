from django.contrib import admin
from django.contrib.auth import get_user_model


class AdminUser(admin.ModelAdmin):
    fields = ("first_name", "last_name", "phone_number", "email", "last_login")
    # inlines = (AddressInline,) # اضافه کردن آدرس‌ها به صفحه کاربر
    search_fields = (
        "phone_number",
        "first_name",
        "last_name",
    )
admin.site.register(get_user_model(), AdminUser)
