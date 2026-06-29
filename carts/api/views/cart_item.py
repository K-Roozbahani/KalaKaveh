from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from carts.api.serializers import (
    AddCartItemSerializer,
    CartSerializer,
    UpdateCartItemSerializer,
)
from carts.models import CartItem
from carts.selectors import get_user_active_cart
from carts.services.cart import (
    add_to_cart,
    get_or_create_cart,
    remove_cart_item,
    update_cart_item,
)
from carts.services.totals import calculate_cart_totals


class CartItemViewSet(GenericViewSet):

    permission_classes = [IsAuthenticated]

    def _get_cart(self, user):
        """
        دریافت سبد فعال کاربر.

        در صورت عدم وجود سبد، سبد جدید ایجاد می‌شود.
        """

        cart = get_user_active_cart(user)

        if cart:
            return cart

        return get_or_create_cart(user=user)

    def _get_cart_response(self, cart):
        """
        ساخت خروجی استاندارد سبد خرید.
        """

        totals = calculate_cart_totals(cart)

        serializer = CartSerializer(cart)

        return {
            "cart": serializer.data,
            "totals": totals,
        }

    def create(self, request):
        """
        افزودن کالا به سبد خرید.
        """

        serializer = AddCartItemSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        cart = self._get_cart(request.user)

        add_to_cart(
            cart=cart,
            variant=serializer.validated_data["variant"],
            quantity=serializer.validated_data["quantity"],
        )

        return Response(
            self._get_cart_response(cart),
            status=status.HTTP_201_CREATED,
        )

    def partial_update(self, request, pk):
        """
        تغییر تعداد یک آیتم در سبد خرید.
        """

        cart = self._get_cart(request.user)

        item = get_object_or_404(
            CartItem,
            pk=pk,
            cart=cart,
        )

        serializer = UpdateCartItemSerializer(
            data=request.data,
            context={"cart_item": item},
        )

        serializer.is_valid(raise_exception=True)

        update_cart_item(
            item=item,
            quantity=serializer.validated_data["quantity"],
        )

        return Response(
            self._get_cart_response(cart),
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, pk):
        """
        حذف آیتم از سبد خرید.
        """

        cart = self._get_cart(request.user)

        item = get_object_or_404(
            CartItem,
            pk=pk,
            cart=cart,
        )

        remove_cart_item(item)

        return Response(
            self._get_cart_response(cart),

            status=status.HTTP_200_OK,
        )