from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound

from products.models import (
    Product,
    ProductVariant,
    Review,
)
from products.selectors import get_product_by_slug


@transaction.atomic
def create_product(
    *,
    name: str,
    description: str = "",
    category=None,
    brand=None,
    is_active: bool = True,
) -> Product:
    """
    ایجاد محصول
    """

    return Product.objects.create(
        name=name,
        description=description,
        category=category,
        brand=brand,
        is_active=is_active,
    )


@transaction.atomic
def update_product(
    *,
    product: Product,
    **data,
) -> Product:
    """
    بروزرسانی محصول
    """

    for field, value in data.items():
        setattr(
            product,
            field,
            value,
        )

    product.save(
        update_fields=data.keys(),
    )

    return product


@transaction.atomic
def create_product_variant(
    *,
    product: Product,
    sku: str,
    price: int,
    stock: int = 0,
    discount_amount: int = 0,
    final_price: int | None = None,
    is_active: bool = True,
) -> ProductVariant:
    """
    ایجاد تنوع محصول
    """

    if final_price is None:
        final_price = max(
            price - discount_amount,
            0,
        )

    return ProductVariant.objects.create(
        product=product,
        sku=sku,
        price=price,
        discount_amount=discount_amount,
        final_price=final_price,
        stock=stock,
        is_active=is_active,
    )


@transaction.atomic
def update_product_variant(
    *,
    variant: ProductVariant,
    **data,
) -> ProductVariant:
    """
    بروزرسانی تنوع محصول
    """

    for field, value in data.items():
        setattr(
            variant,
            field,
            value,
        )

    variant.save(
        update_fields=data.keys(),
    )

    return variant


@transaction.atomic
def create_review(
    *,
    product: Product,
    user,
    rating: int,
    comment: str = "",
) -> Review:
    """
    ثبت نظر محصول
    """

    review, _ = Review.objects.update_or_create(
        product=product,
        user=user,
        defaults={
            "rating": rating,
            "comment": comment,
        },
    )

    return review

def prepare_retrieve_product_by_slug(
    *,
    slug: str,
) -> Product:
    """
    آماده‌سازی اطلاعات محصول برای نمایش جزئیات.

    Raises:
        NotFound: اگر محصول با اسلاگ موردنظر یافت نشود.
    """

    product = get_product_by_slug(slug=slug)

    if product is None:
        raise NotFound(_("محصول مورد نظر یافت نشد."))

    return product
