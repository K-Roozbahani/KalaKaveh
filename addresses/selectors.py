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


def get_default_address(*, user):
    """
    دریافت آدرس پیش‌فرض کاربر
    """

    return (
        Address.objects
        .filter(user=user, is_default=True)
        .select_related("province", "city")
        .first()
    )


def get_address_by_id(*, user, address_id: int):
    """
    دریافت یک آدرس متعلق به کاربر (security safe)
    """

    return (
        Address.objects
        .filter(id=address_id, user=user)
        .select_related("province", "city")
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


