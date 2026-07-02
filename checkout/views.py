from django.urls import reverse

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from carts.api.serializers  import CartSerializer

from discounts.selectors import get_coupon_by_code

from addresses.selectors import (
    get_address_by_id,
)

from addresses.api.serializers import AddressDetailSerializer

from shipping.serializers import ShippingMethodSerializer

from shipping.services.shipping_method import (
    get_available_shipping_methods_for_order,
)

from checkout.serializers import (
    CheckoutCreateSerializer,
)

from checkout.services import start_checkout

from carts.selectors import get_user_active_cart


class CheckoutView(APIView):
    """
    نهایی‌سازی خرید و ورود به فرآیند پرداخت
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        نمایش اطلاعات نهایی Checkout
        """

        address_id = request.query_params.get("address_id")

        if not address_id:
            return Response(
                {
                    "detail": "address_id is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart = get_user_active_cart(request.user)

        address = get_address_by_id(
            address_id=address_id,
        )

        shipping_methods = (
            get_available_shipping_methods_for_order(
                cart=cart,
                address=address,
            )
        )

        return Response(
            {
                "cart": CartSerializer(cart).data,
                "address": AddressDetailSerializer(address).data,
                "shipping_methods": ShippingMethodSerializer(
                    shipping_methods,
                    many=True,
                ).data,
            }
        )

    def post(self, request):

        serializer = CheckoutCreateSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        coupon = None

        coupon_code = serializer.validated_data.get(
            "coupon",
        )

        if coupon_code:
            coupon = get_coupon_by_code(
                coupon_code,
            )

        callback_url = request.build_absolute_uri(
            reverse(
                "payments:payment-callback",
            )
        )

        payment = start_checkout(
            user=request.user,
            address_id=serializer.validated_data[
                "address_id"
            ],
            shipping_method_id=serializer.validated_data[
                "shipping_method_id"
            ],
            gateway=serializer.validated_data[
                "gateway"
            ],
            callback_url=callback_url,
            coupon=coupon,
            note=serializer.validated_data.get(
                "note",
                "",
            ),
        )

        return Response(
            {
                "payment_url": payment.payment_url,
            },
            status=status.HTTP_201_CREATED,
        )