from django.test import TestCase
from django.contrib.auth import get_user_model

from products.selectors import (
    get_categories,
    get_category_by_slug,
    get_brands,
    get_brand_by_slug,
    get_active_products,
    get_product_by_slug,
    get_product_by_id,
    get_variant_by_id,
    get_variant_by_sku,
    get_product_variants,
    get_product_reviews,
    get_product_images,
    get_variant_images,
)

from products.models import (
    ProductImage,
    VariantImage,
)

from products.tests.factories import (
    create_category,
    create_brand,
    create_product,
    create_variant,
    create_review,
)

User = get_user_model()


class CategorySelectorsTest(TestCase):

    def test_get_categories(self):

        category = create_category()

        queryset = get_categories()

        self.assertIn(
            category,
            queryset,
        )

    def test_get_category_by_slug(self):

        category = create_category(
            slug="mobile",
        )

        result = get_category_by_slug(
            slug="mobile",
        )

        self.assertEqual(
            result.pk,
            category.pk,
        )

    class BrandSelectorsTest(TestCase):

        def test_get_brands(self):
            brand = create_brand()

            queryset = get_brands()

            self.assertIn(
                brand,
                queryset,
            )

        def test_get_brand_by_slug(self):
            brand = create_brand(
                slug="samsung",
            )

            result = get_brand_by_slug(
                slug="samsung",
            )

            self.assertEqual(
                result.pk,
                brand.pk,
            )

    class ProductSelectorsTest(TestCase):

        def test_get_active_products(self):
            active_product = create_product(
                is_active=True,
            )

            create_product(
                is_active=False,
            )

            queryset = get_active_products()

            self.assertIn(
                active_product,
                queryset,
            )

            self.assertEqual(
                queryset.count(),
                1,
            )

        def test_get_product_by_slug(self):
            product = create_product(
                slug="iphone-15",
            )

            result = get_product_by_slug(
                slug="iphone-15",
            )

            self.assertEqual(
                result.pk,
                product.pk,
            )

        def test_get_product_by_id(self):
            product = create_product()

            result = get_product_by_id(
                product_id=product.id,
            )

            self.assertEqual(
                result.pk,
                product.pk,
            )

    class VariantSelectorsTest(TestCase):

        def test_get_variant_by_id(self):
            variant = create_variant()

            result = get_variant_by_id(
                variant_id=variant.id,
            )

            self.assertEqual(
                result.pk,
                variant.pk,
            )

        def test_get_variant_by_sku(self):
            variant = create_variant(
                sku="SKU-TEST",
            )

            result = get_variant_by_sku(
                sku="SKU-TEST",
            )

            self.assertEqual(
                result.pk,
                variant.pk,
            )

        def test_get_product_variants(self):
            product = create_product()

            variant = create_variant(
                product=product,
            )

            queryset = get_product_variants(
                product_id=product.id,
            )

            self.assertIn(
                variant,
                queryset,
            )

    class ReviewSelectorsTest(TestCase):

        def test_get_product_reviews(self):
            user = User.objects.create_user(
                phone_number="+989121111111",
                password="123456",
            )

            product = create_product()

            review = create_review(
                user=user,
                product=product,
            )

            queryset = get_product_reviews(
                product_id=product.id,
            )

            self.assertIn(
                review,
                queryset,
            )

    class ProductImageSelectorsTest(TestCase):

        def test_get_product_images(self):
            product = create_product()

            image = ProductImage.objects.create(
                product=product,
                image="test.jpg",
            )

            queryset = get_product_images(
                product_id=product.id,
            )

            self.assertIn(
                image,
                queryset,
            )

    class VariantImageSelectorsTest(TestCase):

        def test_get_variant_images(self):
            variant = create_variant()

            image = VariantImage.objects.create(
                variant=variant,
                image="test.jpg",
            )

            queryset = get_variant_images(
                variant_id=variant.id,
            )

            self.assertIn(
                image,
                queryset,
            )

