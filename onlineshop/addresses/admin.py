from django.contrib import admin

from .models import Province, City, Address


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "name",
    )


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "province",
    )

    list_filter = (
        "province",
    )

    search_fields = (
        "name",
        "province__name",
    )

    autocomplete_fields = (
        "province",
    )

    ordering = (
        "province",
        "name",
    )



@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "receiver_name",
        "receiver_phone",
        "user",
        "province",
        "city",
        "is_default",
        "created_at",
    )

    list_filter = (
        "is_default",
        "address_type",
        "province",
        "city",
        "created_at",
    )

    search_fields = (
        "title",
        "receiver_name",
        "receiver_phone",
        "postal_code",
        "user__phone_number",
        "user__first_name",
        "user__last_name",
    )

    autocomplete_fields = (
        "user",
        "province",
        "city",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "اطلاعات کاربر",
            {
                "fields": (
                    "user",
                )
            },
        ),
        (
            "اطلاعات گیرنده",
            {
                "fields": (
                    "receiver_name",
                    "receiver_phone",
                )
            },
        ),
        (
            "آدرس",
            {
                "fields": (
                    "title",
                    "address_type",
                    "province",
                    "city",
                    "address_line",
                    "plaque",
                    "unit",
                    "postal_code",
                    "description",
                )
            },
        ),
        (
            "تنظیمات",
            {
                "fields": (
                    "is_default",
                )
            },
        ),
        (
            "زمان‌ها",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )





