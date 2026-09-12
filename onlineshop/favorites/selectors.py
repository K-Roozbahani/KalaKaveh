from django.db.models import Prefetch

from favorites.models import Favorite
from products.models import ProductVariant


def list_user_favorites(
    *,
    user,
):
    """
    دریافت لیست محصولات مورد علاقه کاربر.

    فقط محصولات و Variantهای فعال دریافت می‌شوند.
    اطلاعات لازم برای نمایش قیمت نیز از قبل Prefetch می‌شوند.
    """

    default_variants = (
        ProductVariant.objects
        .filter(
            is_active=True,
        )
        .order_by(
            "final_price",
            "-stock",
            "id",
        )
    )

    return (
        Favorite.objects
        .filter(
            user=user,
            product__is_active=True,
        )
        .select_related(
            "product",
            "product__brand",
            "product__category",
        )
        .prefetch_related(
            Prefetch(
                "product__variants",
                queryset=default_variants,
            )
        )
        .order_by("-created_at")
    )

def get_favorite_by_id(
    *,
    user,
    favorite_id: int,
):
    """
    دریافت یک علاقه‌مندی متعلق به کاربر.

    فقط محصولات فعال و Variantهای فعال دریافت می‌شوند.
    """

    return (
        Favorite.objects
        .filter(
            id=favorite_id,
            user=user,
        )
        .first()
    )