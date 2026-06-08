from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from products.models import ProductVariant

from carts.models import CartItem

from carts.api.serializers import (
    AddCartItemSerializer,
    UpdateCartItemSerializer,
)

from carts.services.cart import (
    add_to_cart,
    get_or_create_cart,
    remove_cart_item,
    update_cart_item,
)


class CartItemViewSet(GenericViewSet):

    permission_classes = IsAuthenticated

    def create(self, request, *args, **kwargs):

        serializer = AddCartItemSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        variant = get_object_or_404(
            ProductVariant,
            pk=serializer.validated_data["variant_id"]
        )

        cart = get_or_create_cart(user=request.user)

        add_to_cart(
            cart=cart,
            variant=variant,
            quantity=serializer.validated_data[
                "quantity"
            ],
        )

        return Response(status=status.HTTP_201_CREATED)

    def partial_update(
        self,
        request,
        pk=None,
    ):

        cart = get_or_create_cart(
            user=request.user
        )

        item = get_object_or_404(
            CartItem,
            pk=pk,
            cart=cart,
        )

        serializer = (
            UpdateCartItemSerializer(
                data=request.data,
                context={
                    "cart_item": item
                }
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        update_cart_item(
            item=item,
            quantity=serializer.validated_data[
                "quantity"
            ],
        )

        return Response(
            status=status.HTTP_200_OK
        )


    def destroy(
        self,
        request,
        pk=None,
    ):

        cart = get_or_create_cart(
            user=request.user
        )

        item = get_object_or_404(
            CartItem,
            pk=pk,
            cart=cart,
        )

        remove_cart_item(
            item
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

