from django.contrib import admin
from django.contrib.auth import get_user_model

from users.models import Blacklist


class AdminUser(admin.ModelAdmin):
    fields = ("first_name", "last_name", "phone_number", "email", "last_login")
    # inlines = (AddressInline,) # اضافه کردن آدرس‌ها به صفحه کاربر
    search_fields = (
        "phone_number",
        "first_name",
        "last_name",
    )
admin.site.register(get_user_model(), AdminUser)



@admin.register(Blacklist)
class BlacklistAdmin(admin.ModelAdmin):
    """
    مدیریت لیست سیاه.
    """

    list_display = (
        "phone_number",
        "ip_address",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "phone_number",
        "ip_address",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 50

    fieldsets = (
        (
            "اطلاعات",
            {
                "fields": (
                    "phone_number",
                    "ip_address",
                    "is_active",
                ),
            },
        ),
        (
            "زمان‌ها",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )
