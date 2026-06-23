from django.test import TestCase
from django.contrib.auth import get_user_model

from products.services.product import (
    create_product as create_product_service,
    update_product,
    create_product_variant,
    update_product_variant,
    create_review,
)

from products.tests.factories import (
    create_category,
    create_brand,
    create_product,
    create_variant,
)

User = get_user_model()


class ProductServiceTest(TestCase):

    def test_create_product(self):

        category = create_category()

        brand = create_brand()

        product = create_product_service(
            name="گوشی سامسونگ",
            description="توضیحات تست",
            category=category,
            brand=brand,
        )

        self.assertEqual(
            product.name,
            "گوشی سامسونگ",
        )

        self.assertEqual(
            product.description,
            "توضیحات تست",
        )

        self.assertEqual(
            product.category,
            category,
        )

        self.assertEqual(
            product.brand,
            brand,
        )

        self.assertTrue(
            product.is_active,
        )

    def test_update_product(self):

        product = create_product()

        updated_product = update_product(
            product=product,
            name="محصول جدید",
            description="توضیحات جدید",
        )

        self.assertEqual(
            updated_product.name,
            "محصول جدید",
        )

        self.assertEqual(
            updated_product.description,
            "توضیحات جدید",
        )


class ProductVariantServiceTest(TestCase):

    def test_create_product_variant(self):

        product = create_product()

        variant = create_product_variant(
            product=product,
            sku="SKU-TEST",
            price=100000,
            stock=10,
        )

        self.assertEqual(
            variant.product,
            product,
        )

        self.assertEqual(
            variant.sku,
            "SKU-TEST",
        )

        self.assertEqual(
            variant.price,
            100000,
        )

        self.assertEqual(
            variant.stock,
            10,
        )

        self.assertTrue(
            variant.is_active,
        )

    def test_update_product_variant(self):

        variant = create_variant(
            price=100000,
            stock=10,
        )

        updated_variant = update_product_variant(
            variant=variant,
            price=200000,
            stock=20,
        )

        self.assertEqual(
            updated_variant.price,
            200000,
        )

        self.assertEqual(
            updated_variant.stock,
            20,
        )


class ReviewServiceTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            phone_number="+989121111111",
            password="123456",
        )

        self.product = create_product()

    def test_create_review(self):

        review = create_review(
            product=self.product,
            user=self.user,
            rating=5,
            comment="عالی بود",
        )

        self.assertEqual(
            review.product,
            self.product,
        )

        self.assertEqual(
            review.user,
            self.user,
        )

        self.assertEqual(
            review.rating,
            5,
        )

        self.assertEqual(
            review.comment,
            "عالی بود",
        )

    def test_update_existing_review(self):

        create_review(
            product=self.product,
            user=self.user,
            rating=5,
            comment="نظر اول",
        )

        review = create_review(
            product=self.product,
            user=self.user,
            rating=3,
            comment="نظر جدید",
        )

        self.assertEqual(
            review.rating,
            3,
        )

        self.assertEqual(
            review.comment,
            "نظر جدید",
        )

        self.assertEqual(
            self.product.reviews.count(),
            1,
        )