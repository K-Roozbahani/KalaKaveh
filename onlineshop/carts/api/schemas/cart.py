from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

from carts.api.serializers import CartSerializer


cart_schema = extend_schema_view(
    list=extend_schema(
        tags=["Cart"],
        summary="نمایش سبد خرید",
        responses={
            200: CartSerializer,
        },
    ),
    clear=extend_schema(
        tags=["Cart"],
        summary="پاک کردن سبد خرید",
        request=None,
        responses={
            200: CartSerializer,
        },
    ),
)