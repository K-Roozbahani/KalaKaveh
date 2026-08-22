from rest_framework import status

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

from carts.api.serializers import (
    AddCartItemSerializer,
    CartSerializer,
    UpdateCartItemSerializer,
)


cart_item_schema = extend_schema_view(
    create=extend_schema(
        tags=["Cart"],
        summary="افزودن آیتم",
        request=AddCartItemSerializer,
        responses={
            status.HTTP_201_CREATED: CartSerializer,
        },
    ),
    partial_update=extend_schema(
        tags=["Cart"],
        summary="ویرایش آیتم",
        request=UpdateCartItemSerializer,
        responses={
            status.HTTP_200_OK: CartSerializer,
        },
    ),
    destroy=extend_schema(
        tags=["Cart"],
        summary="حذف آیتم",
        request=None,
        responses={
            status.HTTP_200_OK: CartSerializer,
        },
    ),
)