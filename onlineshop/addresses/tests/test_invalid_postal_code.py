from django.urls import reverse

from rest_framework import status

from addresses.tests.factories import province_factory, city_factory

def test_invalid_postal_code(self):
    province = province_factory()
    city = city_factory(province)

    payload = {
        "title": "خانه",
        "receiver_name": "علی رضایی",
        "receiver_phone": "+989121111111",
        "province": province.id,
        "city": city.id,
        "address_line": "تهران",
        "postal_code": "1234",
    }

    response = self.client.post(
        reverse("addresses-list"),
        payload,
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_400_BAD_REQUEST,
    )

    self.assertIn(
        "postal_code",
        response.data,
    )