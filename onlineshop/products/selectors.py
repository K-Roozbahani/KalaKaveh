from collections import defaultdict

from django.db.models import (
    Prefetch,
    QuerySet,
    Subquery,
    OuterRef
)
from django.db.models.aggregates import Avg, Count

from .models import (
    Product,
    ProductVariant,
    Category,
    Brand,
    Review,
    ProductImage,
    VariantImage,
    ProductVariantAttribute,
    ProductVariantAttributeProperty,
    ProductAttributeValue,
    ProductAttributeValueProperty,
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
) -> Category | None:
    """
    دریافت دسته‌بندی بر اساس اسلاگ
    """

    return Category.objects.filter(
        slug=slug,
    ).first()

def get_category_descendants(*, category: Category) -> list[Category]:
    """
    دریافت دسته‌بندی و تمام زیرمجموعه‌های آن.

    این تابع تمام دسته‌بندی‌ها را تنها با یک Query از دیتابیس
    دریافت کرده و سپس پیمایش درخت را در حافظه انجام می‌دهد.
    """

    all_categories = Category.objects.only(
        "id",
        "parent_id",
    )

    children_map = defaultdict(list)

    for item in all_categories:
        children_map[item.parent_id].append(item)

    result = []

    def collect(node: Category):
        result.append(node)

        for child in children_map[node.id]:
            collect(child)

    collect(category)
    result.reverse()
    return result


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
) -> Brand | None:
    """
    دریافت برند بر اساس اسلاگ
    """

    return Brand.objects.filter(
        slug=slug,
    ).first()


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
    دریافت محصولات برای صفحه لیست فروشگاه.

    برای هر محصول، Variant پیش‌فرض بر اساس:
        1- کمترین قیمت
        2- بیشترین موجودی
        3- کمترین شناسه

    انتخاب شده و قیمت آن به صورت Annotation
    روی محصول قرار می‌گیرد.
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

    default_variant = (
        ProductVariant.objects
        .filter(
            product=OuterRef("pk"),
            is_active=True,
        )
        .order_by(
            "final_price",
            "-stock",
            "id",
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
        .annotate(
            default_price=Subquery(
                default_variant.values("final_price")[:1],
            ),
        )
    )


def get_product_detail_by_slug(
    *,
    slug: str,
) -> Product | None:
    """
    دریافت اطلاعات کامل محصول برای صفحه جزئیات.
    """

    variant_attributes = (
        ProductVariantAttribute.objects
        .select_related(
            "attribute",
        )
        .prefetch_related(
            Prefetch(
                "properties",
                queryset=ProductVariantAttributeProperty.objects.all(),
            )
        )
    )

    variants = (
        ProductVariant.objects
        .filter(
            is_active=True,
        )
        .prefetch_related(
            "images",
            Prefetch(
                "attributes",
                queryset=variant_attributes,
                to_attr="prefetched_attributes",
            ),
        )
    )

    attribute_values = (
        ProductAttributeValue.objects
        .select_related(
            "attribute",
        )
        .prefetch_related(
            Prefetch(
                "properties",
                queryset=ProductAttributeValueProperty.objects.all(),
            )
        )
        .order_by(
            "sort_order",
            "id",
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
                to_attr="prefetched_variants",
            ),

            # تمام مشخصات محصول
            Prefetch(
                "attribute_values",
                queryset=attribute_values,
                to_attr="prefetched_attribute_values",
            ),

            # ویژگی‌های شاخص
            Prefetch(
                "attribute_values",
                queryset=attribute_values.filter(
                    is_highlight=True,
                ),
                to_attr="highlight_attributes",
            ),
        )
        .filter(
            slug=slug,
            is_active=True,
        )
        .first()
    )


def get_product_by_slug(
    *,
    slug: str,
) -> Product| None:
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
        .filter(
            slug=slug,
            is_active=True,
        ).first()
    )


def get_product_by_id(
    *,
    product_id: int,
) -> Product | None:
    """
    دریافت محصول بر اساس شناسه
    """

    return Product.objects.filter(
        pk=product_id,
    ).first()


# =====================================================
# Variant
# =====================================================

def get_variant_by_id(
    *,
    variant_id: int,
) -> ProductVariant | None:
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
        .filter(
            pk=variant_id,
        ).first()
    )


def get_variant_by_sku(
    *,
    sku: str,
) -> ProductVariant | None:
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
        .filter(
            sku=sku,
        ).first()
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

def get_product_review_summary(
    *,
    product_id: int,
) -> dict:
    """
    دریافت خلاصه آماری امتیازهای محصول.
    """

    reviews = Review.objects.filter(
        product_id=product_id,
        is_valid=True,
    )

    summary = reviews.aggregate(
        average_rate=Avg("rating"),
        total_count=Count("id"),
    )

    counts = {}

    for rate in range(1, 6):
        count = reviews.filter(
            rating=rate,
        ).count()

        if count:
            counts[str(rate)] = count

    return {
        "average_rate": round(
            summary["average_rate"] or 0,
            1,
        ),
        "total_count": summary["total_count"],
        "counts": counts,
    }

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
) -> Review | None:
    """
    دریافت نظر بر اساس شناسه
    """

    return (
        Review.objects
        .select_related(
            "product",
            "user",
        )
        .filter(
            pk=review_id,
        ).first()
    )

def get_user_review(
    *,
    product: Product,
    user,
) -> Review | None:
    """
    دریافت نظر کاربر برای یک محصول
    """

    return (
        Review.objects
        .select_related(
            "product",
            "user",
        )
        .filter(
            product=product,
            user=user,
        ).first()
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