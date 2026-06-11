from addresses.models import Province, City, Address


def province_factory(name="تهران"):
    return Province.objects.create(
        name=name,
    )


def city_factory(province=None, name="تهران"):
    if province is None:
        province = province_factory()

    return City.objects.create(
        province=province,
        name=name,
    )


def address_factory(user, **kwargs):
    province = kwargs.pop("province", None)

    if province is None:
        province = province_factory()

    city = kwargs.pop("city", None)

    if city is None:
        city = city_factory(province=province)

    defaults = {
        "title": "خانه",
        "receiver_name": "علی رضایی",
        "receiver_phone": "+989121111111",
        "province": province,
        "city": city,
        "address_line": "تهران، خیابان آزادی",
        "plaque": "10",
        "unit": "2",
        "postal_code": "1234567890",
        "is_default": False,
    }

    defaults.update(kwargs)

    return Address.objects.create(
        user=user,
        **defaults,
    )