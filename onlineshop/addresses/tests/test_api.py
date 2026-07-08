from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from addresses.tests.factories import address_factory

User = get_user_model()


class AddressApiTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            phone_number="+989121111123",
            password="123456",
        )

        self.client.force_authenticate(
            user=self.user,
        )

    def test_list_addresses(self):
        address_factory(self.user)

        response = self.client.get(
            reverse("addresses-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_retrieve_address(self):
        address = address_factory(self.user)

        response = self.client.get(
            reverse(
                "addresses-detail",
                kwargs={"pk": address.id},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_delete_address(self):
        address = address_factory(self.user)

        response = self.client.delete(
            reverse(
                "addresses-detail",
                kwargs={"pk": address.id},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

    def test_set_default_address(self):
        address = address_factory(self.user)

        response = self.client.post(
            reverse(
                "addresses-set-default",
                kwargs={"pk": address.id},
            )
        )

        address.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            address.is_default,
        )

    def test_user_cannot_access_other_user_address(self):
        other_user = User.objects.create_user(
            phone_number="+989121111124",
            password="123456",
        )

        address = address_factory(other_user)

        response = self.client.get(
            reverse(
                "addresses-detail",
                kwargs={"pk": address.id},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_anonymous_user_cannot_access_addresses(self):
        self.client.force_authenticate(
            user=None,
        )

        response = self.client.get(
            reverse("addresses-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )