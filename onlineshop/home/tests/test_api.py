from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase


class HomePageAPIViewTests(APITestCase):

    def test_returns_status_200(self):
        response = self.client.get(
            reverse("home:home-page"),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_anonymous_user_can_access(self):
        response = self.client.get(
            reverse("home:home-page"),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_returns_list(self):
        response = self.client.get(
            reverse("home:home-page"),
        )

        self.assertIsInstance(
            response.data,
            list,
        )