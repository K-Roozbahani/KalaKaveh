from django.db.models import QuerySet, Prefetch

from .models import (
    Product,
    ProductVariant,
    Category,
    Brand,
    Review,
    ProductImage,
    VariantImage,
)


def get_categories() -> QuerySet[Category]:
    """
    دریافت تمام دسته‌بندی‌ها
    """

    return Category.objects.all()


def get_category_by_slug(*, slug: str) -> Category:
    """
    دریافت دسته‌بندی بر اساس اسلاگ
    """

    return Category.objects.get(
        slug=slug,
    )

def get_brands() -> QuerySet[Brand]:
    """
    دریافت تمام برندها
    """

    return Brand.objects.all()


def get_brand_by_slug(*, slug: str) -> Brand:
    """
    دریافت برند بر اساس اسلاگ
    """

    return Brand.objects.get(
        slug=slug,
    )

def get_active_products() -> QuerySet[Product]:
    """
    دریافت محصولات فعال
    """

    return Product.objects.filter(
        is_active=True,
    )

def get_product_by_slug(*, slug: str) -> Product:
    """
    دریافت محصول بر اساس اسلاگ
    """

    return (
        Product.objects
        .select_related(
            "category",
            "brand",
        )
        .prefetch_related(
            "images",
            "variants",
            "attribute_values",
        )
        .get(
            slug=slug,
            is_active=True,
        )
    )

def get_product_by_id(*, product_id: int) -> Product:
    """
    دریافت محصول بر اساس شناسه
    """

    return Product.objects.get(
        pk=product_id,
    )


def get_variant_by_id(
    *,
    variant_id: int,
) -> ProductVariant:
    """
    دریافت تنوع محصول
    """

    return (
        ProductVariant.objects
        .select_related(
            "product",
        )
        .get(
            pk=variant_id,
        )
    )


def get_variant_by_sku(
    *,
    sku: str,
) -> ProductVariant:
    """
    دریافت تنوع بر اساس SKU
    """

    return (
        ProductVariant.objects
        .select_related(
            "product",
        )
        .get(
            sku=sku,
        )
    )


def get_product_variants(
    *,
    product_id: int,
) -> QuerySet[ProductVariant]:
    """
    دریافت تنوع‌های محصول
    """

    return (
        ProductVariant.objects
        .filter(
            product_id=product_id,
            is_active=True,
        )
    )


def get_product_reviews(
    *,
    product_id: int,
) -> QuerySet[Review]:
    """
    دریافت نظرات محصول
    """

    return (
        Review.objects
        .select_related(
            "user",
        )
        .filter(
            product_id=product_id,
        )
    )


def get_product_images(
    *,
    product_id: int,
) -> QuerySet[ProductImage]:
    """
    تصاویر محصول
    """

    return ProductImage.objects.filter(
        product_id=product_id,
    )


def get_variant_images(
    *,
    variant_id: int,
) -> QuerySet[VariantImage]:
    """
    تصاویر تنوع محصول
    """

    return VariantImage.objects.filter(
        variant_id=variant_id,
    )


