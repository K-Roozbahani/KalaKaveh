from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError

from addresses import selectors

from addresses.tests.factories import address_factory
from orders.services.validators import validate_address_owner

User = get_user_model()


class AddressSelectorTests(TestCase):

    def test_get_user_addresses(self):
        user1 = User.objects.create_user(
            phone_number="+989121111117",
            password="123456",
        )

        user2 = User.objects.create_user(
            phone_number="+989121111118",
            password="123456",
        )

        address_factory(user1)
        address_factory(user2)

        addresses = selectors.get_user_addresses(
            user=user1,
        )

        self.assertEqual(
            addresses.count(),
            1,
        )

    def test_get_default_address(self):
        user = User.objects.create_user(
            phone_number="+989121111119",
            password="123456",
        )

        address = address_factory(
            user,
            is_default=True,
        )

        result = selectors.get_default_address(
            user=user,
        )

        self.assertEqual(
            result.id,
            address.id,
        )

    def test_get_address_by_id(self):
        user = User.objects.create_user(
            phone_number="+989121111120",
            password="123456",
        )

        address = address_factory(user)

        result = selectors.get_address_by_id(
            address_id=address.id,
        )

        self.assertEqual(
            result.id,
            address.id,
        )

    def test_get_address_by_id_other_user(self):
        user1 = User.objects.create_user(
            phone_number="+989121111121",
            password="123456",
        )

        user2 = User.objects.create_user(
            phone_number="+989121111122",
            password="123456",
        )

        address = address_factory(user2)

        with self.assertRaises(ValidationError):
            validate_address_owner(
                address,
                user1,
            )