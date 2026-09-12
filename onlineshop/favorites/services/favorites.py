from django.db import IntegrityError, transaction
from rest_framework.exceptions import ValidationError

from favorites.models import Favorite
from favorites.selectors import get_favorite_by_id
from products.models import Product


@transaction.atomic
def add_favorite(
    *,
    user,
    product: Product,
) -> Favorite:
    """
    افزودن محصول به علاقه‌مندی‌های کاربر.
    """

    if not product.is_active:
        raise ValidationError(
            {
                "product": "این محصول در حال حاضر فعال نیست.",
            }
        )

    try:
        favorite, _ = Favorite.objects.get_or_create(
            user=user,
            product=product,
        )
    except IntegrityError:
        # در شرایط درخواست هم‌زمان، رکورد موجود را دریافت می‌کنیم.
        favorite = Favorite.objects.get(
            user=user,
            product=product,
        )

    return favorite


@transaction.atomic
def remove_favorite(
    *,
    user,
    favorite_id: int,
) -> None:
    """
    حذف علاقه‌مندی کاربر.
    """

    favorite = get_favorite_by_id(
        user=user,
        favorite_id=favorite_id,
    )

    if favorite is None:
        raise ValidationError(
            {
                "detail": "این علاقه‌مندی یافت نشد.",
            }
        )

    favorite.delete()