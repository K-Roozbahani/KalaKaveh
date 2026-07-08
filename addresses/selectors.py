from django.db.models import QuerySet

from addresses.models import Address, Province, City

def get_user_addresses(*, user):
    """
    دریافت همه آدرس‌های یک کاربر
    """

    return (
        Address.objects
        .filter(user=user)
        .select_related("province", "city", "user")
        .order_by("-is_default", "-created_at")
    )


def get_default_address(*, user,
                        addresses: QuerySet | None = None
                        ):
    """
    دریافت آدرس پیش‌فرض کاربر
    """
    if addresses is not None:
        return (
            addresses
            .filter(is_default=True)
            .first()
        )

    return (
        Address.objects
        .filter(user=user, is_default=True)
        .select_related("province", "city")
        .first()
    )


def get_address_by_id(*,
                      address_id: int,
                      addresses: QuerySet | None = None,
                      ):
    """
    دریافت یک آدرس متعلق به کاربر (security safe)
    """
    if addresses is not None:
        return (
            addresses.filter(id=address_id).first()
        )

    return (
        Address.objects
        .select_related(
            "province",
            "city",
        )
        .filter(pk=address_id)
        .first()
    )


def get_provinces():
    """
    لیست استان‌ها (برای فرم‌ها)
    """

    return Province.objects.all().order_by("name")


def get_cities_by_province(*, province):
    """
    شهرهای یک استان (Cascading dropdown)
    """

    return (
        City.objects
        .filter(province=province)
        .order_by("name")
    )


def get_city_by_id(*, city_id: int):
    """
    گرفتن شهر با id
    """

    return (
        City.objects
        .filter(id=city_id)
        .select_related("province")
        .first()
    )


