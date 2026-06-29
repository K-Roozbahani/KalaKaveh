from decimal import Decimal

import factory
from factory.django import DjangoModelFactory

from accounts.models import User
from brands.models import Brand
from carts.models import (
    Cart,
    CartItem,
)
from products.models import (
    Category,
    Product,
    ProductVariant,
)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    phone_number = factory.Sequence(
        lambda n: f"+989120000{n:04d}"
    )

    password = factory.PostGenerationMethodCall(
        "set_password",
        "123456",
    )


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    title = factory.Sequence(
        lambda n: f"دسته {n}"
    )

    slug = factory.Sequence(
        lambda n: f"category-{n}"
    )


class BrandFactory(DjangoModelFactory):
    class Meta:
        model = Brand

    title = factory.Sequence(
        lambda n: f"برند {n}"
    )

    slug = factory.Sequence(
        lambda n: f"brand-{n}"
    )


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    category = factory.SubFactory(
        CategoryFactory,
    )

    brand = factory.SubFactory(
        BrandFactory,
    )

    title = factory.Sequence(
        lambda n: f"محصول {n}"
    )

    slug = factory.Sequence(
        lambda n: f"product-{n}"
    )

    is_active = True


class ProductVariantFactory(DjangoModelFactory):
    class Meta:
        model = ProductVariant

    product = factory.SubFactory(
        ProductFactory,
    )

    sku = factory.Sequence(
        lambda n: f"SKU-{n}"
    )

    price = Decimal("100000")

    stock = 10

    is_active = True


class CartFactory(DjangoModelFactory):
    class Meta:
        model = Cart

    user = factory.SubFactory(
        UserFactory,
    )


class CartItemFactory(DjangoModelFactory):
    class Meta:
        model = CartItem

    cart = factory.SubFactory(
        CartFactory,
    )

    variant = factory.SubFactory(
        ProductVariantFactory,
    )

    quantity = 1