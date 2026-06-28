
from django.urls import reverse
from rest_framework.test import APITestCase

from products.tests.factories import (
    create_product,
    create_variant,
    create_category,
    create_brand,
)



class ProductAPITests(APITestCase):

    def setUp(self):

        self.category = create_category(
            name="موبایل",
        )

        self.brand = create_brand(
            name="اپل",
        )

        self.product = create_product(
            name="iPhone 15",
            category=self.category,
            brand=self.brand,
        )

        self.variant1 = create_variant(
            product=self.product,
            price=100000,
            final_price=90000,
            stock=0,
        )

        self.variant2 = create_variant(
            product=self.product,
            price=120000,
            final_price=110000,
            stock=5,
        )

    def test_product_list_api(self):

        url = reverse("product-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.data["results"]), 1)

        product = response.data[0]

        self.assertEqual(product["name"], "iPhone 15")

        self.assertIn("final_price", product)
        self.assertIn("price", product)
        self.assertIn("discount_amount", product)