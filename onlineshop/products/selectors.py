from django.db.models import (
    Prefetch,
    QuerySet,
)

from .models import (
    Product,
    ProductVariant,
    Category,
    Brand,
    Review,
    ProductImage,
    VariantImage,
)


# =====================================================
# Category
# =====================================================

def get_categories() -> QuerySet[Category]:
    """
    دریافت تمام دسته‌بندی‌ها
    """

    return Category.objects.all()


def get_category_by_slug(
    *,
    slug: str,
) -> Category:
    """
    دریافت دسته‌بندی بر اساس اسلاگ
    """

    return Category.objects.get(
        slug=slug,
    )


# =====================================================
# Brand
# =====================================================

def get_brands() -> QuerySet[Brand]:
    """
    دریافت تمام برندها
    """

    return Brand.objects.all()


def get_brand_by_slug(
    *,
    slug: str,
) -> Brand:
    """
    دریافت برند بر اساس اسلاگ
    """

    return Brand.objects.get(
        slug=slug,
    )


# =====================================================
# Product
# =====================================================

def get_active_products() -> QuerySet[Product]:
    """
    دریافت محصولات فعال
    """

    return Product.objects.filter(
        is_active=True,
    )


def get_products_for_listing() -> QuerySet[Product]:
    """
    دریافت محصولات برای صفحه لیست فروشگاه
    """

    variants = (
        ProductVariant.objects
        .filter(
            is_active=True,
        )
        .order_by(
            "final_price",
            "-stock",
            "id",
        )
        .prefetch_related(
            "images",
        )
    )

    return (
        Product.objects
        .filter(
            is_active=True,
        )
        .select_related(
            "category",
            "brand",
        )
        .prefetch_related(
            "images",
            Prefetch(
                "variants",
                queryset=variants,
            ),
        )
    )


def get_product_detail_by_slug(
    *,
    slug: str,
) -> Product:
    """
    دریافت اطلاعات کامل محصول برای صفحه جزئیات
    """

    variants = (
        ProductVariant.objects
        .filter(
            is_active=True,
        )
        .prefetch_related(
            "images",
        )
    )

    return (
        Product.objects
        .select_related(
            "category",
            "brand",
        )
        .prefetch_related(
            "images",
            Prefetch(
                "variants",
                queryset=variants,
            ),
            "attribute_values__attribute",
            "reviews__user",
        )
        .get(
            slug=slug,
            is_active=True,
        )
    )


def get_product_by_slug(
    *,
    slug: str,
) -> Product:
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


def get_product_by_id(
    *,
    product_id: int,
) -> Product:
    """
    دریافت محصول بر اساس شناسه
    """

    return Product.objects.get(
        pk=product_id,
    )


# =====================================================
# Variant
# =====================================================

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
        .prefetch_related(
            "images",
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
    دریافت تنوع محصول بر اساس SKU
    """

    return (
        ProductVariant.objects
        .select_related(
            "product",
        )
        .prefetch_related(
            "images",
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
    دریافت تنوع‌های فعال محصول
    """

    return (
        ProductVariant.objects
        .filter(
            product_id=product_id,
            is_active=True,
        )
        .prefetch_related(
            "images",
        )
        .order_by(
            "-stock",
            "final_price",
            "id",
        )
    )


def get_default_variant(
    *,
    product: Product,
) -> ProductVariant | None:
    """
    دریافت Variant پیش‌فرض محصول

    این تابع هیچ Query جدیدی ایجاد نمی‌کند
    در صورتی که variants قبلاً Prefetch شده باشند.
    """

    variants = list(
        product.variants.all()
    )

    if not variants:
        return None

    return variants[0]


# =====================================================
# Review
# =====================================================

def get_product_reviews(
    *,
    product_id: int,
):
    """
    دریافت نظرات تایید شده محصول
    """

    return (
        Review.objects
        .select_related("user")
        .filter(
            product_id=product_id,
            is_valid=True,
        )
        .order_by("-created_at")
    )

def get_review_by_id(
    *,
    review_id: int,
) -> Review:
    """
    دریافت نظر بر اساس شناسه
    """

    return (
        Review.objects
        .select_related(
            "product",
            "user",
        )
        .get(
            pk=review_id,
        )
    )

def get_user_review(
    *,
    product: Product,
    user,
) -> Review:
    """
    دریافت نظر کاربر برای یک محصول
    """

    return (
        Review.objects
        .select_related(
            "product",
            "user",
        )
        .get(
            product=product,
            user=user,
        )
    )


# =====================================================
# Images
# =====================================================

def get_product_images(
    *,
    product_id: int,
) -> QuerySet[ProductImage]:
    """
    دریافت تصاویر محصول
    """

    return (
        ProductImage.objects
        .filter(
            product_id=product_id,
        )
    )


def get_variant_images(
    *,
    variant_id: int,
) -> QuerySet[VariantImage]:
    """
    دریافت تصاویر تنوع محصول
    """

    return (
        VariantImage.objects
        .filter(
            variant_id=variant_id,
        )
    )

# =====================================================
# Primary Images
# =====================================================

def get_primary_product_image(
    *,
    product,
) -> ProductImage | None:
    """
    دریافت تصویر اصلی محصول

    در صورت نبود تصویر اصلی، اولین تصویر محصول
    برگردانده می‌شود.
    """

    image = (
        ProductImage.objects
        .filter(
            product=product,
            is_primary=True,
        )
        .first()
    )

    if image:
        return image

    return (
        ProductImage.objects
        .filter(
            product=product,
        )
        .first()
    )


def get_primary_variant_image(
    *,
    variant,
) -> VariantImage | None:
    """
    دریافت تصویر اصلی تنوع محصول

    در صورت نبود تصویر اصلی، اولین تصویر تنوع
    برگردانده می‌شود.
    """

    image = (
        VariantImage.objects
        .filter(
            variant=variant,
            is_primary=True,
        )
        .first()
    )

    if image:
        return image

    return (
        VariantImage.objects
        .filter(
            variant=variant,
        )
        .first()
    )