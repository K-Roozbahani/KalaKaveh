from drf_spectacular.utils import extend_schema, extend_schema_view

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from carts.selectors import get_cart_item_by_id
from carts.api.serializers import (
    AddCartItemSerializer,
    UpdateCartItemSerializer,
    CartSerializer,
)

from carts.services.cart import (
    add_to_cart,
    update_cart_item,
    remove_cart_item,
    get_or_create_cart,
)

from carts.services.pricing import calculate_cart_totals


@extend_schema_view(
    create=extend_schema(tags=["Cart"], summary="افزودن آیتم"),
    partial_update=extend_schema(tags=["Cart"], summary="ویرایش آیتم"),
    destroy=extend_schema(tags=["Cart"], summary="حذف آیتم"),
)
class CartItemViewSet(ViewSet):

    permission_classes = [AllowAny]

    # =====================================================
    # Helpers
    # =====================================================

    def get_cart(self):

        if not self.request.session.session_key:
            self.request.session.create()

        return get_or_create_cart(
            user=self.request.user if self.request.user.is_authenticated else None,
            session_key=self.request.session.session_key,
        )

    def get_cart_item(self):

        item = get_cart_item_by_id(
            item_id=self.kwargs["pk"],
            user=self.request.user if self.request.user.is_authenticated else None,
            session_key=self.request.session.session_key,
        )

        if item is None:
            raise NotFound()

        return item

    def cart_response(self, cart, status_code=status.HTTP_200_OK):

        serializer = CartSerializer(
            cart,
            context={
                "pricing": calculate_cart_totals(cart=cart),
            },
        )

        return Response(serializer.data, status=status_code)

    # =====================================================
    # CREATE
    # =====================================================

    def create(self, request):

        serializer = AddCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = self.get_cart()

        add_to_cart(
            cart=cart,
            **serializer.validated_data,
        )

        return self.cart_response(cart=cart, status_code=status.HTTP_201_CREATED)

    # =====================================================
    # UPDATE (IMPORTANT FIX HERE)
    # =====================================================

    def partial_update(self, request, pk=None):

        # ❗️ FIRST: ownership check (critical fix)
        item = self.get_cart_item()

        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        update_cart_item(
            item=item,
            **serializer.validated_data,
        )

        return self.cart_response(cart=self.get_cart())

    # =====================================================
    # DELETE
    # =====================================================

    def destroy(self, request, pk=None):

        item = self.get_cart_item()

        remove_cart_item(item=item)

        return self.cart_response(cart=self.get_cart())