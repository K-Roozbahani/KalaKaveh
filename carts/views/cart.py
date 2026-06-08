from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from carts.api.serializers import ApplyCouponSerializer, CartSerializer

from carts.services.cart import get_or_create_cart

from carts.services.coupon import apply_coupon

from carts.services.totals import calculate_cart_totals


class CartViewSet(GenericViewSet):

    permission_classes = [IsAuthenticated]

    serializer_class = CartSerializer

    def list(self, request, *args, **kwargs):

        cart = get_or_create_cart(user=request.user)

        totals = calculate_cart_totals(cart)

        serializer = self.get_serializer(cart)

        data = serializer.data

        data.update(totals)

        return Response(data)



    @action(detail=False, methods=["post"])
    def apply_coupon(self, request):

        serializer = ApplyCouponSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        cart = get_or_create_cart(user=request.user)

        apply_coupon(cart=cart, code=serializer.validated_data["code"])

        totals = calculate_cart_totals(cart)

        return Response(totals, status=status.HTTP_200_OK)


    @action(detail=False, methods=["delete"])
    def remove_coupon(self, request):

        cart = get_or_create_cart(user=request.user)

        cart.coupon = None

        cart.save(update_fields=["coupon"])

        totals = calculate_cart_totals(cart)

        return Response(totals, status=status.HTTP_200_OK)

