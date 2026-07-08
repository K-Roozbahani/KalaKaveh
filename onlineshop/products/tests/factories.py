import uuid

from products.models import (
    Category,
    Brand,
    Product,
    ProductVariant,
    Review,
)


def create_category(**kwargs):
    return Category.objects.create(
        name=kwargs.get(
            "name",
            "دسته تست",
        ),
        slug=kwargs.get(
            "slug",
            f"category-{Category.objects.count() + 1}",
        ),
        parent=kwargs.get(
            "parent",
        ),
    )


def create_brand(**kwargs):
    return Brand.objects.create(
        name=kwargs.get(
            "name",
            "برند تست",
        ),
        slug=kwargs.get(
            "slug",
            f"brand-{Brand.objects.count() + 1}",
        ),
    )


def create_product(**kwargs):

    category = kwargs.pop(
        "category",
        None,
    )

    if category is None:
        category = create_category()

    brand = kwargs.pop(
        "brand",
        None,
    )

    if brand is None:
        brand = create_brand()

    return Product.objects.create(
        name=kwargs.get(
            "name",
            "محصول تست",
        ),
        slug=kwargs.get(
            "slug",
            f"product-{Product.objects.count() + 1}",
        ),
        description=kwargs.get(
            "description",
            "توضیحات تست",
        ),
        category=category,
        brand=brand,
        is_active=kwargs.get(
            "is_active",
            True,
        ),
    )


def create_variant(**kwargs):

    product = kwargs.pop(
        "product",
        None,
    )

    if product is None:
        product = create_product()

    return ProductVariant.objects.create(
        product=product,
        sku=kwargs.get(
            "sku",
            f"SKU-{uuid.uuid4().hex[:8]}",
        ),
        price=kwargs.get(
            "price",
            100000,
        ),
        discount_amount=kwargs.get(
            "discount_amount",
            0,
        ),
        final_price=kwargs.get(
            "final_price",
            100000,
        ),
        stock=kwargs.get(
            "stock",
            10,
        ),
        is_active=kwargs.get(
            "is_active",
            True,
        ),
    )


def create_review(
    *,
    user,
    **kwargs,
):
    product = kwargs.pop(
        "product",
        None,
    )

    if product is None:
        product = create_product()

    return Review.objects.create(
        product=product,
        user=user,
        rating=kwargs.get(
            "rating",
            5,
        ),
        comment=kwargs.get(
            "comment",
            "نظر تست",
        ),
    )