from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from addresses.models import Address
from .factories import province_factory, city_factory

User = get_user_model()


def test_postal_code_validation():
    user = User.objects.create_user(
        phone_number="+989121111111",
        password="123456",
    )

    province = province_factory()
    city = city_factory(province)

    address = Address(
        user=user,
        title="خانه",
        receiver_name="علی رضایی",
        receiver_phone="+989121111111",
        province=province,
        city=city,
        address_line="تهران",
        postal_code="1234",
    )

    try:
        address.full_clean()
    except ValidationError:
        assert True
    else:
        assert False