from django.contrib.auth import get_user_model
from django.test import TestCase

from addresses.services.address import (
    create_address,
    update_address,
    delete_address,
    set_default_address,
)

from .factories import (
    province_factory,
    city_factory,
    address_factory,
)

User = get_user_model()


class AddressServiceTests(TestCase):

    def test_create_first_address_is_default(self):
        user = User.objects.create_user(
            phone_number="+989121111111",
            password="123456",
        )

        province = province_factory()
        city = city_factory(province)

        address = create_address(
            user=user,
            title="خانه",
            receiver_name="علی",
            receiver_phone="+989121111111",
            province=province,
            city=city,
            address_line="تهران",
            postal_code="1234567890",
        )

        self.assertTrue(address.is_default)

    def test_create_second_address_not_default(self):
        user = User.objects.create_user(
            phone_number="+989121111112",
            password="123456",
        )

        address_factory(user, is_default=True)

        address = address_factory(user)

        self.assertFalse(address.is_default)

    def test_update_address(self):
        user = User.objects.create_user(
            phone_number="+989121111113",
            password="123456",
        )

        address = address_factory(user)

        update_address(
            address=address,
            title="محل کار",
        )

        address.refresh_from_db()

        self.assertEqual(
            address.title,
            "محل کار",
        )

    def test_set_default_address(self):
        user = User.objects.create_user(
            phone_number="+989121111114",
            password="123456",
        )

        address1 = address_factory(
            user,
            is_default=True,
        )

        address2 = address_factory(user)

        set_default_address(
            address=address2,
        )

        address1.refresh_from_db()
        address2.refresh_from_db()

        self.assertFalse(address1.is_default)
        self.assertTrue(address2.is_default)

    def test_user_has_only_one_default_address(self):
        user = User.objects.create_user(
            phone_number="+989121111115",
            password="123456",
        )

        address1 = address_factory(
            user,
            is_default=True,
        )

        address2 = address_factory(user)

        set_default_address(
            address=address2,
        )

        count = user.addresses.filter(
            is_default=True
        ).count()

        self.assertEqual(count, 1)

    def test_delete_default_address_assigns_new_default(self):
        user = User.objects.create_user(
            phone_number="+989121111116",
            password="123456",
        )

        address1 = address_factory(
            user,
            is_default=True,
        )

        address2 = address_factory(user)

        delete_address(
            address=address1,
        )

        address2.refresh_from_db()

        self.assertTrue(address2.is_default)