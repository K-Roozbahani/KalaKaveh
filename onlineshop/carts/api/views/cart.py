from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from carts.api.serializers import CartSerializer

from carts.services.cart import (
    clear_cart,
    get_or_create_cart,
)

from carts.services.pricing import (
    calculate_cart_totals,
)


@extend_schema_view(
    list=extend_schema(
        tags=["Cart"],
        summary="نمایش سبد خرید",
    ),
    clear=extend_schema(
        tags=["Cart"],
        summary="پاک کردن سبد خرید",
    ),
)
class CartViewSet(ViewSet):

    permission_classes = [
        AllowAny,
    ]

    pagination_class = None

    # =====================================================
    # Helpers
    # =====================================================

    def get_cart(self):

        if not self.request.session.session_key:
            self.request.session.create()

        return get_or_create_cart(
            user=(
                self.request.user
                if self.request.user.is_authenticated
                else None
            ),
            session_key=self.request.session.session_key,
        )

    def cart_response(
        self,
        *,
        cart,
        status_code=status.HTTP_200_OK,
    ):

        serializer = CartSerializer(
            cart,
            context={
                "pricing": calculate_cart_totals(
                    cart=cart,
                ),
            },
        )

        return Response(
            serializer.data,
            status=status_code,
        )

    # =====================================================
    # API
    # =====================================================

    def list(
        self,
        request,
    ):

        return self.cart_response(
            cart=self.get_cart(),
        )

    @action(
        detail=False,
        methods=["delete"],
    )
    def clear(
        self,
        request,
    ):

        cart = self.get_cart()

        clear_cart(
            cart=cart,
        )

        return self.cart_response(
            cart=cart,
        )