from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from carts.selectors import (
    get_cart_item_by_id,
)

from carts.api.serializers import (
    AddCartItemSerializer,
    CartSerializer,
    UpdateCartItemSerializer,
)

from carts.services.cart import (
    add_to_cart,
    clear_cart,
    get_or_create_cart,
    remove_cart_item,
    update_cart_item,
)

from carts.services.pricing import (
    calculate_cart_totals,
)


@extend_schema_view(
    retrieve=extend_schema(
        summary="نمایش سبد خرید",
    ),
)
class CartViewSet(GenericViewSet):

    def get_cart(self):

        return get_or_create_cart(
            user=self.request.user,
        )

    def get_serializer_class(self):

        if self.action == "add_item":
            return AddCartItemSerializer

        if self.action == "update_item":
            return UpdateCartItemSerializer

        return CartSerializer

    def retrieve(self, request, *args, **kwargs):

        cart = self.get_cart()

        pricing = calculate_cart_totals(
            cart=cart,
        )

        serializer = self.get_serializer(
            cart,
            context={
                "pricing": pricing,
            },
        )

        return Response(serializer.data)

    @action(
        detail=False,
        methods=["post"],
        url_path="items",
    )
    def add_item(self, request):

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        cart = self.get_cart()

        add_to_cart(
            cart=cart,
            **serializer.validated_data,
        )

        pricing = calculate_cart_totals(
            cart=cart,
        )

        return Response(
            CartSerializer(
                cart,
                context={
                    "pricing": pricing,
                },
            ).data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=True,
        methods=["patch"],
        url_path="items",
    )
    def update_item(
        self,
        request,
        pk=None,
    ):

        item = get_cart_item_by_id(
            pk=pk,
            cart=self.get_cart(),
        )

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        update_cart_item(
            item=item,
            **serializer.validated_data,
        )

        cart = self.get_cart()

        pricing = calculate_cart_totals(
            cart=cart,
        )

        return Response(
            CartSerializer(
                cart,
                context={
                    "pricing": pricing,
                },
            ).data,
        )

    @action(
        detail=True,
        methods=["delete"],
        url_path="items",
    )
    def remove_item(
        self,
        request,
        pk=None,
    ):

        item = get_cart_item_by_id(
            pk=pk,
            cart=self.get_cart(),
        )

        remove_cart_item(
            item=item,
        )

        cart = self.get_cart()

        pricing = calculate_cart_totals(
            cart=cart,
        )

        return Response(
            CartSerializer(
                cart,
                context={
                    "pricing": pricing,
                },
            ).data,
        )

    @action(
        detail=False,
        methods=["delete"],
    )
    def clear(self, request):

        cart = self.get_cart()

        clear_cart(
            cart=cart,
        )

        pricing = calculate_cart_totals(
            cart=cart,
        )

        return Response(
            CartSerializer(
                cart,
                context={
                    "pricing": pricing,
                },
            ).data,
        )

