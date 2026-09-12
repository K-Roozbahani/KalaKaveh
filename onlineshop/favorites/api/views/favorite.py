from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils.api.views import BaseGenericViewSet

from favorites.api.schemas.favorrite import favorite_schema
from favorites.api.serializers.favorite import (
    FavoriteAddSerializer,
    FavoriteListSerializer,
)
from favorites.selectors import (
    list_user_favorites,
)
from favorites.services.favorites import (
    add_favorite,
    remove_favorite,
)
from products.selectors import get_product_by_id

@favorite_schema
class FavoriteViewSet(BaseGenericViewSet):
    """
    API علاقه‌مندی‌های کاربر.
    """

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        انتخاب Serializer متناسب با نوع درخواست.
        """

        if self.action == "list":
            return FavoriteListSerializer

        if self.action == "create":
            return FavoriteAddSerializer

        return FavoriteListSerializer

    def list(self, request, *args, **kwargs):
        """
        دریافت لیست علاقه‌مندی‌های کاربر.
        """

        favorites = list_user_favorites(
            user=request.user,
        )

        serializer = self.get_serializer(
            favorites,
            many=True,
        )

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        افزودن محصول به علاقه‌مندی‌های کاربر.
        """

        serializer = self.get_serializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        product = get_product_by_id(
            product_id=serializer.validated_data["product_id"],
        )

        favorite = add_favorite(
            user=request.user,
            product=product,
        )

        return Response(
            FavoriteListSerializer(
                favorite,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
        )

    def destroy(self, request, *args, **kwargs):
        """
        حذف علاقه‌مندی کاربر.
        """

        remove_favorite(
            user=request.user,
            favorite_id=kwargs["pk"],
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )